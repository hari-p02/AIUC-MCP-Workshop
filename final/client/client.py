import asyncio
import json
import os
from typing import Optional
from contextlib import AsyncExitStack
import yaml
from mcp import ClientSession
from mcp.client.sse import sse_client

from anthropic import Anthropic
from dotenv import load_dotenv
load_dotenv("../../.env")

# load_dotenv("/Users/haripat/Desktop/SF/mcp_demo/.env")  # change this path

class MCPClient:
    def __init__(self, name: str):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.messages = []
        self.name = name
        self.system_prompt = "You are a helpful assistant that can help with a users personal finances. You carefully explain any action you have taken."
        
    async def connect_to_sse_server(self, server_url: str):
        """Connect to an MCP server running with SSE transport"""
        self._streams_context = sse_client(url=server_url)
        streams = await self._streams_context.__aenter__()

        self._session_context = ClientSession(*streams)
        self.session: ClientSession = await self._session_context.__aenter__()

        await self.session.initialize()

        print("Initialized SSE client...")

    async def cleanup(self):
        """Properly clean up the session and streams"""
        if self._session_context:
            await self._session_context.__aexit__(None, None, None)
        if self._streams_context:
            await self._streams_context.__aexit__(None, None, None)
    
    async def get_current_tool_names(self):
        response = await self.session.list_tools()
        available_tool_names = [tool.name for tool in response.tools]
        return available_tool_names
    
    async def chat_loop(self):
        while True:
            user_question = input("Enter a question: ")
            self.messages.append({
                "role": "user",
                "content": user_question
            })
            response = await self.session.list_tools()

            # for tool in response.tools:
            #     print(tool.name)
            #     print(tool.description)
            #     print(tool.inputSchema)

            available_tools = [{ 
                                    "name": tool.name,
                                    "description": tool.description,
                                    "input_schema": tool.inputSchema
                                } for tool in response.tools]

            response = self.anthropic.messages.create(
                model="claude-3-7-sonnet-20250219",
                max_tokens=1000,
                system=self.system_prompt,
                messages=self.messages,
                tools=available_tools
            )

            tool_results = []
            final_text = []

            for content in response.content:
                if content.type == 'text':
                    final_text.append(content.text)
                elif content.type == 'tool_use':
                    tool_name = content.name
                    tool_args = content.input
                    
                    result = await self.session.call_tool(tool_name, tool_args)
                    tool_results.append({"call": tool_name, "result": result})
                    final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                    self.messages.append({
                        "role": "assistant", 
                        "content": f"Calling tool {tool_name} with args {tool_args}, the reuslt is: " + "\n".join([x.text for x in result.content])
                    })


                    response = self.anthropic.messages.create(
                        model="claude-3-7-sonnet-20250219",
                        max_tokens=1000,
                        system=self.system_prompt,
                        messages=self.messages,
                    )
                    print("FIRST RESPONSE", response)
                    try:
                        final_text.append(response.content[0].text)
                        print(final_text[-1])
                    except Exception as e:
                        print(e)

async def main(name, server_url):
    client = MCPClient(name=name)
    try:
        await client.connect_to_sse_server(server_url=server_url)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys
    asyncio.run(main(name=sys.argv[1], server_url=sys.argv[2]))