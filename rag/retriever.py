from langchain_chroma import Chroma

from providers.embedding_provider import get_embeddings



CHROMA_PATH="chroma_db"



def get_retriever():


    embeddings = get_embeddings()


    vectorstore = Chroma(

        persist_directory=CHROMA_PATH,

        embedding_function=embeddings

    )


    retriever = vectorstore.as_retriever(

        search_type="similarity",

        search_kwargs={
            "k":5
        }

    )


    return retriever