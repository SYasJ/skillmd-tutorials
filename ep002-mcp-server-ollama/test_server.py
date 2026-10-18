import asyncio
import sys

from mcp import Client, StdioServerParameters


async def main() -> None:
    server = StdioServerParameters(command=sys.executable, args=["server.py"])
    async with Client(server) as client:
        tools = (await client.list_tools()).tools
        print("TOOLS:", [t.name for t in tools])
        result = await client.call_tool("repo_stats", {"repo": "ollama/ollama"})
        print("RESULT:", result.content[0].text)


asyncio.run(main())
