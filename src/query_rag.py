from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import time

USE_FAKE_EMBEDDINGS = False  # 🛠️ Change if needed

def query_rag(vectordb, query):
    if USE_FAKE_EMBEDDINGS:
        return "This is a fake answer because you're using Fake Embeddings."
    else: 
        llm = Ollama(
            model="llama3",  # OR 'mistral', 'qwen', etc
           # base_url="http://localhost:11434"
            temperature = 0.2,
            num_ctx = 2048,
            top_p = 0.9
            )

        retriever = vectordb.as_retriever(search_kwargs={"k":5})


        prompt=PromptTemplate.from_template("""
        Answer the question based only on the context below.
        Question:{question}
        Context:
        {context}
    
        If you don't know the answer, say 'I don't know'.
        """ )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt}
        )

        print("Fetching best matching documents......")
        docs=retriever.get_relevant_documents(query)

        print("Generating the answer (using Llama3)....")
        
        for percent in tqdm(range(100), desc="Progress",ncols=80,bar_format='{l_bar}{bar} |{n_fmt}%'):
            time.sleep(0.02)
        

        result = qa_chain.run(query)
        print("\n Answer is Ready!")

        return result
