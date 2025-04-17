import yaml
from client import MCPClient
from anthropic import Anthropic
import os
import asyncio
from dotenv import load_dotenv
load_dotenv("../../.env")

class MultiClient:
    def __init__(self):
        self.clients = []
        self.system_prompt = "You are a helpful assistant that can help with a users personal finances. You carefully explain any action you have taken."
        self.anthropic = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    async def cleanup(self):
        """Cleanup all clients"""
        for client in reversed(self.clients):
            await client.cleanup()

    async def service_tools(self, service_name: str) -> str:
        pass


    async def load_servers(self, servers_file: str):
        """Load servers from a file"""
        with open(servers_file, "r") as f:
            servers = yaml.safe_load(f)

        for server in servers["servers"]:
            await self._add_server(server["name"], server["url"])
            pass
    
    async def _add_server(self, name: str, server_url: str): # should I add a name?
        """Add a client to the manager"""
        pass
    
    def has_tool_use(self, response):
        pass


    async def chat_loop(self):
        pass

async def main():
    client = MultiClient()
    try:
        await client.load_servers(servers_file=os.getenv("SERVER_DETAILS")) # change path
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    import sys
    asyncio.run(main())