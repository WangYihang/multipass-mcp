import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "multipass": {
                "command": "uvx",
                "args": ["multipass-mcp"],
            }
        }
    )
    async for message in query(
        prompt="List all my multipass instances and tell me which ones are running.",
        options=options,
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
