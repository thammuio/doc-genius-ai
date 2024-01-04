from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pydantic import BaseModel
from typing import Any, Union, Optional
from fastapi import HTTPException
from app.chatbot.load_model import load_llama_model
from app.embeddings.chunk_utils import *
from app.utils.constants import ENGINE_NAME
import pinecone


# Store the value of the VECTOR_DB environment variable in a variable
vector_db = os.getenv('VECTOR_DB').upper()

if vector_db == "MILVUS":
    from pymilvus import connections, Collection
    import app.utils.vectordb.start_milvus as vector_db
    import app.embeddings.embeddings_utils as model_embedding

if vector_db == "PINECONE":
    from sentence_transformers import SentenceTransformer

class LazyModel:
    def __init__(self, load_model_func):
        self.load_model_func = load_model_func
        self._model = None

    @property
    def model(self):
        if self._model is None:
            self._model = self.load_model_func()  # Model is loaded here if it hasn't been loaded already
        return self._model

    def __call__(self, *args, **kwargs):
        return self.model(*args, **kwargs)

# This creates a LazyModel instance that will load the model the first time it's used
llama2_model = LazyModel(load_llama_model)

class TextInput(BaseModel):
    inputs: str
    parameters: Union[dict[str, Any], None]


def generate_text(data: TextInput) -> dict[str, str]:
    try:
        engine = ENGINE_NAME
        temperature = 1
        token_count = 100
        
        question = data.inputs
        params = data.parameters or {}
        
        if 'temperature' in params:
            temperature = int(params['temperature'])
            
        if 'max_tokens' in params:
            token_count = int(params['max_tokens'])
            
        if 'engine' in params:
            engine = str(params['engine'])
            
        res = get_responses(engine, temperature, token_count, question)
                            
        return {"response": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Helper function for generating responses for the QA app
def get_responses(engine, temperature, token_count, question):
    if engine == "" or question == "" or engine is None or question is None:
        return "One or more fields have not been specified."
    
    if temperature == "" or temperature is None:
      temperature = 1
      
    if token_count == "" or token_count is None:
      token_count = 100

    if vector_db == "MILVUS":
        # Load Milvus Vector DB collection
        vector_db_collection = Collection('cloudera_docs')
        vector_db_collection.load()
    
    # Phase 1: Get nearest knowledge base chunk for a user question from a vector db
    vdb_question = question
    
    if vector_db == "MILVUS":
        context_chunk = get_nearest_chunk_from_milvus_vectordb(vector_db_collection, vdb_question)
        vector_db_collection.release()

    if vector_db == "PINECONE":
        PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
        PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
        PINECONE_INDEX = os.getenv('PINECONE_INDEX')
        pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
        index = pinecone.Index(PINECONE_INDEX)

        # Get latest statistics from index
        current_collection_stats = index.describe_index_stats()
        print('Total number of embeddings in Pinecone index is {}.'.format(current_collection_stats.get('total_vector_count')))

        context_chunk = get_nearest_chunk_from_pinecone_vectordb(index, vdb_question)
    
    if engine == ENGINE_NAME:
        # Phase 2a: Perform text generation with LLM model using found kb context chunk
        response = get_llama2_response_with_context(question, context_chunk, temperature, token_count)

    return response


  
# Pass through user input to LLM model with enhanced prompt and stop tokens
def get_llama2_response_with_context(question, context, temperature, token_count):
    question = "Answer this question based on given context: " + question + " "
    question_and_context = question + " Here is the context: " + str(context)

    try:
        params = {
            "temperature": float(temperature),
            "max_tokens": int(token_count)
        }
        response = llama2_model(prompt=question_and_context, **params)

        model_out = response['choices'][0]['text']
        return model_out
    
    except Exception as e:
        print(e)
        return e