from agent.agent import get_agent


async def ask_admin(question: str):

    agent = await get_agent()


    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )


    return response["messages"][-1].content