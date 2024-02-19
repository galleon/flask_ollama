# Import modules
import chromadb
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

# Create Chroma DB client and access the existing vector store
client = chromadb.PersistentClient(path="./chroma_db_data")
chroma_collection = client.get_or_create_collection(name="tweets")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# Initialize Ollama and ServiceContext
llm = Ollama(model="mistral")
service_context = ServiceContext.from_defaults(llm=llm, embed_model="local")

# Create VectorStoreIndex with a similarity threshold of 20
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context, similarity_top_k=20)

# Set up Flask server
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/chat', methods=['GET', 'POST'])
@cross_origin()
def chat():
    query = request.args.get('query') if request.method == 'GET' else request.form.get('query')
    if query is not None:
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return jsonify({"response": str(response)})
    else:
        return jsonify({"error": "query field is missing"}), 400
    
if __name__ == '__main__':
    app.run()
