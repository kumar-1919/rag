from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

USE_FAKE_EMBEDDINGS = False  # 🛠️ Change if needed

def query_rag(vectordb, query):
    if USE_FAKE_EMBEDDINGS:
        return "This is a fake answer because you're using Fake Embeddings."
    else:
        llm = Ollama(
            model="llama3",  # OR 'mistral', 'qwen', etc
            base_url="http://localhost:11434"
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectordb.as_retriever()
        )

        result = qa_chain.run(query)
        return result
