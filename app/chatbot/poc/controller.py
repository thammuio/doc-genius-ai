from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pydantic import BaseModel
from typing import Any, Union, Optional
from fastapi import HTTPException
from app.chatbot.poc.load_model import load_llama_model
from app.embeddings.chunk_utils import *
from app.utils.constants import ENGINE_NAME
import pinecone
if os.getenv('VECTOR_DB').upper() == "MILVUS":
    from pymilvus import connections, Collection
    import app.utils.vectordb.start_milvus as vector_db
    import app.embeddings.embeddings_utils as model_embedding

if os.getenv('VECTOR_DB').upper() == "PINECONE":
    from sentence_transformers import SentenceTransformer

class TextInput(BaseModel):
    inputs: str
    parameters: Union[dict[str, Any], None]

