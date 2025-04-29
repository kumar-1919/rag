from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from tqdm import tqdm
import os
 
def create_embeddings(documents):
    # Load Ollama embeddings
    embedding_function = OllamaEmbeddings(
        model="nomic-embed-text" , # Make sure this model is pulled
        base_url = "http://20.220.168.11:11434"
    )
    
    # Directory to store the database
    persist_directory = "db"
    
    # Load or initialize Chroma DB
    if os.path.exists(persist_directory):
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding_function)
    else:
        vectordb = Chroma.from_documents([], embedding_function, persist_directory=persist_directory)

    # Get already existing document IDs
    existing_ids = set()
    try:
        if vectordb._collection.count() > 0:
            existing_docs = vectordb.get(include=["metadatas"])
            existing_ids = set(existing_docs["ids"])
    except:
        existing_ids = set()

    # Prepare new docs list
    new_docs = []
    new_ids = []

    # Build new docs avoiding duplicates
    for idx, doc in enumerate(tqdm(documents, desc="Checking Documents")):
        doc_id = f"doc_{idx}"
        if doc_id not in existing_ids:
            new_docs.append(doc)
            new_ids.append(doc_id)

    # Now embed new docs
    if new_docs:
        for idx in tqdm(range(len(new_docs)), desc="Embedding New Documents"):
            vectordb.add_documents([new_docs[idx]], ids=[new_ids[idx]])
            vectordb.persist()
    else:
        print("✅ All documents already embedded!")

    return vectordb
