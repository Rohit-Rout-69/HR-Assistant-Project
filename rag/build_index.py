from rag.ingestion import load_documents

from rag.splitter import split_documents

from rag.vectorstore import create_vectorstore



DATA_PATH="data\documents"



def main():


    print("Loading documents...")

    documents = load_documents(
        DATA_PATH
    )


    print(
        "Documents:",
        len(documents)
    )


    print("Splitting documents...")


    chunks = split_documents(
        documents
    )


    print(
        "Chunks:",
        len(chunks)
    )


    print(
        "Creating vector database..."
    )


    create_vectorstore(
        chunks
    )


    print(
        "Done!"
    )



if __name__=="__main__":

    main()