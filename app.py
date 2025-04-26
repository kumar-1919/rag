from src.load_documents import load_and_split_docs
from src.create_embeddings import create_embeddings
from src.query_rag import query_rag

if __name__ == "__main__":
    documents = load_and_split_docs()
    vectordb = create_embeddings(documents)

    while True:
        query = input("\nAsk your question (type 'exit' to quit): ")
        if query.lower() == "exit":
            break

        result = query_rag(vectordb, query)
        print("\nAnswer:", result)
 