import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    options = ClaudeAgentOptions(
        disallowed_tools=['Bash', 'Edit', 'Grep'],
        mcp_servers={
            "multipass": {
                "command": "uvx",
                "args": ["multipass-mcp"],
            }
        },
        permission_mode="bypassPermissions",
    )

    async for message in query(
        prompt="Create a new multipass instance named 'test-vm' with 2 CPUs and 2GB of memory using Ubuntu 22.04 LTS.",
        options=options,
    ):
        print(message)

if __name__ == "__main__":
    asyncio.run(main())
