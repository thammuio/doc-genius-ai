from pydantic import BaseModel
from typing import Any, Union, Optional
from app.embeddings.chunk_utils import *
import pinecone
import json
import requests
from app.utils.model_access import get_model_access_key, MODEL_API_URL, HEADERS

if os.getenv('VECTOR_DB').upper() == "MILVUS":
    from pymilvus import connections, Collection
    import app.utils.vectordb.start_milvus as vector_db
    import app.embeddings.embeddings_utils as model_embedding

if os.getenv('VECTOR_DB').upper() == "PINECONE":
    from sentence_transformers import SentenceTransformer


# Helper function for generating responses for the QA app
def poc_gpu_rag_llama_2_13b_chat(prompt, temperature, max_tokens, selected_vector_db, user):
    if prompt == "" or temperature == "" or max_tokens is None:
        return "One or more fields have not been specified."
    
    if temperature == "" or temperature is None:
      temperature = 1
      
    if max_tokens == "" or max_tokens is None:
      max_tokens = 100

    if selected_vector_db == "MILVUS":
        # Load Milvus Vector DB collection
        vector_db_collection = Collection('cloudera_docs')
        vector_db_collection.load()

    if user == "" or user is None:
      user = "genius"

    # Step 1: Get nearest knowledge base chunk for a user question from a vector db
    vdb_question = prompt
    
    if selected_vector_db == "MILVUS":
        context_chunk = get_nearest_chunk_from_milvus_vectordb(vector_db_collection, vdb_question)
        vector_db_collection.release()

    if selected_vector_db == "PINECONE":
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
        PINECONE_INDEX = os.getenv('PINECONE_INDEX')
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index(PINECONE_INDEX)

        # Get latest statistics from index
        current_collection_stats = index.describe_index_stats()
        print('Total number of embeddings in Pinecone index is {}.'.format(current_collection_stats.get('total_vector_count')))

        context_chunk = get_nearest_chunk_from_pinecone_vectordb(index, vdb_question)

    # Step 2: Call the relavent Model in Model Serving
    MODEL_ACCESS_KEY = get_model_access_key({"name": "POC LLM Model"})

    question = {'prompt': prompt, "temperature": temperature, "max_tokens": max_tokens, "context": context_chunk, "user": user}
    data = json.dumps({'accessKey': MODEL_ACCESS_KEY, 'request': question})
    response = requests.post(MODEL_API_URL, data = data, headers = HEADERS)
    
    try:
        response_json = response.json()
        return response_json.get('response')
    except json.JSONDecodeError:
        return "Failed to parse JSON response"
