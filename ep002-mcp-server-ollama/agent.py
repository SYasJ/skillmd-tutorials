import asyncio
import os
import sys

import ollama
from mcp import Client, StdioServerParameters

MODEL = os.environ.get("MODEL", "qwen3:4b")
SERVER = StdioServerParameters(command=sys.executable, args=["server.py"])


async def main(question: str, use_tools: bool = True) -> None:
    async with Client(SERVER) as mcp:
        listed = (await mcp.list_tools()).tools
        tools = [
            {"type": "function", "function": {
                "name": t.name, "description": t.description,
                "parameters": t.input_schema}}
            for t in listed
        ] if use_tools else []
        messages = [{"role": "user", "content": question}]
        reply = ollama.chat(MODEL, messages=messages, tools=tools, think=False)
        for call in reply.message.tool_calls or []:
            name, args = call.function.name, call.function.arguments
            print(f"TOOL CALL  {name}({args})")
            result = await mcp.call_tool(name, args)
            text = result.content[0].text
            print(f"TOOL RESULT {text}")
            messages += [reply.message,
                         {"role": "tool", "content": text}]
            reply = ollama.chat(MODEL, messages=messages, think=False)
        answer = reply.message.content.split("</think>")[-1].strip()
        print("ANSWER", answer)


if __name__ == "__main__":
    q = sys.argv[1]
    asyncio.run(main(q, use_tools="--no-tools" not in sys.argv))
