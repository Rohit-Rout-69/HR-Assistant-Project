from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_mcp_tools():

    client = MultiServerMCPClient(
        {
            "hr_server": {

                "command": "python",

                "args": [
                    "-m",
                    "mcp_server.server"
                ],

                "transport": "stdio"

            }
        }
    )


    tools = await client.get_tools()

    return tools