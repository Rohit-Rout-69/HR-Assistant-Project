import asyncio

from agent.agent import get_agent



async def main():


    agent = await get_agent()


    while True:


        question = input(
            "\nAsk HR Assistant: "
        )


        if question.lower()=="exit":
            break


        response = await agent.ainvoke(

            {

                "messages":[

                    {

                    "role":"user",

                    "content":question

                    }

                ]

            }

        )


        print("\nAnswer:")

        print(
            response["messages"][-1].content
        )



if __name__=="__main__":

    asyncio.run(main())