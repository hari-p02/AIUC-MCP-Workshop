from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerHTTP
import logfire
import os
from dotenv import load_dotenv
load_dotenv("../../.env")
logfire.configure(token=os.getenv('LOGFIRE_TOKEN'))

google_mail = MCPServerHTTP(url="http://localhost:8020/sse")
google_sheets = MCPServerHTTP(url="http://localhost:8010/sse")
google_docs = MCPServerHTTP(url="http://localhost:8030/sse")

agent = Agent('anthropic:claude-3-5-sonnet-latest', mcp_servers=[google_mail, google_sheets, google_docs], instrument=True)

async def main():
    async with agent.run_mcp_servers():
        result = await agent.run("hello!")
        while True:
            print(f"\n{result.output}")
            user_input = input("\n> ")
            if 'quit' in user_input: break
            result = await agent.run(user_input, message_history=result.new_messages())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())