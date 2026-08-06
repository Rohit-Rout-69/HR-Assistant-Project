from langchain_chroma import Chroma

from providers.embedding_provider import get_embeddings



CHROMA_PATH = "chroma_db"



def create_vectorstore(chunks):


    embeddings = get_embeddings()


    vectorstore = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=CHROMA_PATH

    )


    return vectorstore