import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        mcp_servers={
            "multipass": {
                "command": "uvx",
                "args": ["multipass-mcp"],
            }
        },
        permission_mode="bypassPermissions",
    )

    async for message in query(
        prompt="List all my multipass images.",
        options=options,
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
