from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from tqdm import tqdm
import time
import re

USE_FAKE_EMBEDDINGS = False  # 🛠️ Change if needed

def format_response(response):
    """
    Function to format the response with numbered points when necessary.
    """
    # Check if the response contains bullet points or steps
    points_pattern = r"(\d+(\.\d+)*\.)\s([^\n]+)"
    steps = re.findall(points_pattern, response)

    if steps:
        # If steps found, format as numbered list
        formatted_response = "\n".join([f"{step[0]} {step[2]}" for step in steps])
    else:
        # If no steps, return the original response as it is
        formatted_response = response
    
    return formatted_response


def query_rag(vectordb, query):
    if USE_FAKE_EMBEDDINGS:
        return "This is a fake answer because you're using Fake Embeddings."
    else: 
        llm = Ollama(
            model="llama3",  # OR 'mistral', 'qwen', etc
            temperature = 0.2,
            num_ctx = 2048,
            top_p = 0.9,
            base_url = "http://20.220.168.11:11434"
        )

        retriever = vectordb.as_retriever(search_kwargs={"k":5})

        prompt = PromptTemplate.from_template("""
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
        docs = retriever.get_relevant_documents(query)

        print("Generating the answer (using Llama3)....")

        # Simulate a loading animation
        for percent in tqdm(range(100), desc="Progress", ncols=80, bar_format='{l_bar}{bar} |{n_fmt}%'):
            time.sleep(0.02)

        result = qa_chain.run(query)
        
        print("\n Answer is Ready!")
        
        # Format the result if it's a structured list of steps
        formatted_result = format_response(result)

        return formatted_result
