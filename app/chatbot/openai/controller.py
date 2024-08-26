from app.embeddings.chunk_utils import *
import pinecone
import json
import requests
import os
from app.chatbot.openai.model import chat_completion

if os.getenv('VECTOR_DB').upper() == "MILVUS":
    from pymilvus import connections, Collection
    import app.utils.vectordb.start_milvus as vector_db
    import app.embeddings.embeddings_utils as model_embedding

if os.getenv('VECTOR_DB').upper() == "PINECONE":
    from sentence_transformers import SentenceTransformer


# Helper function for generating responses for the QA app
def openai_chat(prompt, temperature, max_tokens, selected_vector_db, user):
    if prompt == "" or temperature == "" or max_tokens is None:
        return "One or more fields have not been specified."
    
    if temperature == "" or temperature is None:
      temperature = 1
      
    if max_tokens == "" or max_tokens is None:
      max_tokens = 100

    if selected_vector_db == "MILVUS":
        # Load Milvus Vector DB collection
        vector_db_collection = Collection('retail_kb')
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
        PINECONE_INDEX = os.getenv('PINECONE_INDEX')
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index(PINECONE_INDEX)

        # Get latest statistics from index
        current_collection_stats = index.describe_index_stats()
        print('Total number of embeddings in Pinecone index is {}.'.format(current_collection_stats.get('total_vector_count')))

        context_chunk = get_nearest_chunk_from_pinecone_vectordb(index, vdb_question)


    # question = {'prompt': prompt, "temperature": temperature, "max_tokens": max_tokens, "context": context_chunk, "user": user}
    # Example usage:
    url = os.getenv('CAII_API_URL')
    api_key = os.getenv('CAII_API_KEY')
    model = os.getenv('CAII_MODEL')
    # knowledge_base = "No Returns Accepted: All sales are final. No returns, refunds, or exchanges. If you have any questions, please contact us at"
    knowledge_base = context_chunk
    messages = [
        {"role": "system", "content": f"You are a helpful and knowledgeable retail store assistant. Your role is to assist customers by answering their queries, providing product recommendations, and resolving issues using the latest information from our knowledge base. Here is the Retrieved context from \n{knowledge_base} based on user's questoion. Please answer based on this context only."},
        {"role": "user", "content": f"Customer Question is: \n{prompt}"}
    ]
    # Call OpenAI Model
    # response_dict = 
    response = chat_completion(url, api_key, model, messages)

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
