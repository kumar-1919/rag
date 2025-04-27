from flask import Flask, render_template, request, jsonify
from src.load_documents import load_and_split_docs
from src.create_embeddings import create_embeddings
from src.query_rag import query_rag

app = Flask(__name__)

# Load once when app starts
print("Loading documents and creating embeddings...")
documents = load_and_split_docs()
vectordb = create_embeddings(documents)
print("Embeddings ready!")

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    try:
        bot_response = query_rag(vectordb, user_input)
        return jsonify({'response': bot_response})
    except Exception as e:
        return jsonify({'response': "Sorry, an error occurred!"})

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)