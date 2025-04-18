from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

embedding_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    cache_folder="./hf_model_cache"
)

def process_pdf(filepath, persist_dir):
    loader = PyPDFLoader(filepath)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(texts, embedding_model)
    os.makedirs(persist_dir, exist_ok=True)
    vectorstore.save_local(persist_dir)
    return persist_dir

def load_vectorstore(persist_dir):
    return FAISS.load_local(persist_dir, embedding_model, allow_dangerous_deserialization=True)
