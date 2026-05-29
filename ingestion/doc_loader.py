from langchain_community.document_loaders import Docx2txtLoader


def load_docx(doc_path):
    loader = Docx2txtLoader(doc_path)
    documents = loader.load()
    return documents
