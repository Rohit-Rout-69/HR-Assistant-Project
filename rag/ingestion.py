from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader


def load_documents(data_path):

    loader = DirectoryLoader(
        path=data_path,
        glob="*.pdf",
        loader_cls=PyPDFLoader
    )

    documents = loader.load()

    return documents