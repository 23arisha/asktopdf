from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.indexes import VectorstoreIndexCreator
from langchain_community.embeddings import HuggingFaceEmbeddings

def process_pdf(filepath):
    loader = PyPDFLoader(filepath)
    index = VectorstoreIndexCreator(
        text_splitter=RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100),
        embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2", cache_folder="./hf_model_cache")
    ).from_loaders([loader])
    return index.vectorstore
