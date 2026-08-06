from providers.llm_provider import get_llm

from rag.retriever import get_retriever

from rag.prompts import RAG_PROMPT



def search_hr_policy(question):


    retriever = get_retriever()


    documents = retriever.invoke(
        question
    )


    context = "\n\n".join(
        [
            doc.page_content
            for doc in documents
        ]
    )


    llm = get_llm()


    chain = (
        RAG_PROMPT
        |
        llm
    )


    response = chain.invoke(

        {
            "context":context,

            "question":question
        }

    )


    sources=[]


    for doc in documents:

        sources.append(

            {
                "file":
                doc.metadata.get("source"),

                "page":
                doc.metadata.get("page")

            }

        )


    return {

        "answer":response.content,

        "sources":sources

    }