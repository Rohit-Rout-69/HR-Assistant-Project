from langchain.agents import create_agent
 
from providers.llm_provider import get_llm
 
from agent.prompt import SYSTEM_PROMPT
 
from agent.tools import hr_policy_tool
 
from mcp_client.client import get_mcp_tools
 
 
 
async def get_agent():
 
 
    llm = get_llm()
 
 
    mcp_tools = await get_mcp_tools()
 
 
    # The MCP tools only cover employee/database operations.
    # Add the RAG policy-search tool so the admin agent can also
    # answer HR policy questions grounded in the actual PDFs,
    # instead of falling back on the LLM's own (unverified) knowledge.
    tools = mcp_tools + [hr_policy_tool]
 
 
    agent = create_agent(
 
        model=llm,
 
        tools=tools,
 
        system_prompt=SYSTEM_PROMPT
 
    )
 
 
    return agent