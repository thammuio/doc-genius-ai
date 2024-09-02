from app.embeddings.chunk_utils import *
import pinecone
import json
import requests
import os
from app.chatbot.openai.model import chat_completion
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
def openai_chat(prompt, temperature, max_tokens, selected_vector_db, user):
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


    # Check if prompt contains "truck" followed by a four or five-digit number prefixed with #
    lookup_info_str = None
    try:
        match = re.search(r'LOG-TRK-(\d{4})', prompt)
        if match:
            truck_id = match.group(1)
            lookup_info = lookup_truck_id(truck_id)
            if lookup_info is None:
                lookup_info_str = None
            else:
                lookup_info_str = json.dumps(lookup_info)
    except re.error as regex_error:
        print(f"Regex error: {regex_error}")
        lookup_info_str = None
    except json.JSONDecodeError as json_error:
        print(f"JSON error: {json_error}")
        lookup_info_str = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        lookup_info_str = None

    # question = {'prompt': prompt, "temperature": temperature, "max_tokens": max_tokens, "context": context_chunk, "user": user}
    # Example usage:
    url = os.getenv('CAII_API_URL')
    api_key = os.getenv('CAII_API_KEY')
    model = os.getenv('CAII_MODEL')
    # knowledge_base = "No Returns Accepted: All sales are final. No returns, refunds, or exchanges. If you have any questions, please contact us at"
    knowledge_base = context_chunk

    # Assemble messages
    messages = assemble_messages(prompt, knowledge_base, lookup_info_str)
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
