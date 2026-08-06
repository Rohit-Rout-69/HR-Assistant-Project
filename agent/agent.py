from langchain.agents import create_agent

from providers.llm_provider import get_llm

from agent.prompt import SYSTEM_PROMPT

from mcp_client.client import get_mcp_tools



async def get_agent():


    llm = get_llm()


    mcp_tools = await get_mcp_tools()


    agent = create_agent(

        model=llm,

        tools=mcp_tools,

        system_prompt=SYSTEM_PROMPT

    )


    return agent