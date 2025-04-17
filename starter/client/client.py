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
        pass
    
    async def chat_loop(self):
        while True:
            user_question = input("Enter a question: ")
            pass

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