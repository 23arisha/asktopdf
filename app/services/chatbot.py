import os
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq

def answer_question(vectorstore, query):
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("Missing GROQ_API_KEY")

    llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-8b-8192")

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type="stuff"
    )

    result = qa_chain({"query": query})
    return result["result"]
