from app.embeddings.chunk_utils import *
import pinecone
import json
import requests
import os
from app.chatbot.caii.model import chat_completion
from app.prompts.controller import assemble_messages
from app.agent.lookups import lookup_truck_id
import re

if os.getenv('VECTOR_DB').upper() == "MILVUS":
    from pymilvus import connections, Collection
    import app.utils.vectordb.start_milvus as vector_db
    import app.embeddings.embeddings_utils as model_embedding

if os.getenv('VECTOR_DB').upper() == "PINECONE":
    from sentence_transformers import SentenceTransformer

kb_name = os.getenv('KB_VECTOR_INDEX')

# Helper function for generating responses for the QA app
def caii_chat(prompt, temperature, max_tokens, selected_vector_db, user, model_url, model_name, model_key):
    if prompt == "" or temperature == "" or max_tokens is None:
        return "One or more fields have not been specified."
    
    if temperature == "" or temperature is None:
      temperature = 1
      
    if max_tokens == "" or max_tokens is None:
      max_tokens = 100

    if selected_vector_db == "MILVUS":
        # Load Milvus Vector DB collection
        kb_name = os.getenv('KB_VECTOR_INDEX')
        vector_db_collection = Collection(kb_name)
        vector_db_collection.load()

    if user == "" or user is None:
      user = "genius"

    # Step 1: Get nearest knowledge base chunk for a user question from a vector db
    vdb_question = prompt
    
    if selected_vector_db == "MILVUS":
        context_chunk = get_nearest_chunk_from_milvus_vectordb(vector_db_collection, vdb_question)
        vector_db_collection.release()
        print(context_chunk)

    if selected_vector_db == "PINECONE":
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
        PINECONE_INDEX = os.getenv('KB_VECTOR_INDEX')
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index(PINECONE_INDEX)

        # Get latest statistics from index
        current_collection_stats = index.describe_index_stats()
        print('Total number of embeddings in Pinecone index is {}.'.format(current_collection_stats.get('total_vector_count')))

        context_chunk = get_nearest_chunk_from_pinecone_vectordb(index, vdb_question)

    knowledge_base = context_chunk

    # Assemble messages
    messages = assemble_messages(prompt, knowledge_base)
    # Call CAAI Model
    response = chat_completion(model_url, model_key, model_name, messages)

    if "error" in response:
        # Handle error
        print(f"Error: {response['message']}")
        return json.dumps({"answer": "Something went wrong! Try again later!"})
    else:
        # Handle successful response
        completion = response['choices'][0]['message']['content']
        print(f"Chatbot response: {completion}")
        return {"answer": completion}

    # except Exception as e:
    #     return json.dumps({"answer": "Something went wrong! Try again later!"})
