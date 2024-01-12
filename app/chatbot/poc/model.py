from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pydantic import BaseModel
from typing import Any, Union, Optional
from fastapi import HTTPException
from app.chatbot.poc.load_model import load_llama_model
from app.embeddings.chunk_utils import *
import warnings
warnings.filterwarnings("ignore")
import json


llama2_model = load_llama_model()


# Pass through user input to LLM model with enhanced prompt and stop tokens

def generate_response(json_input):
    try:
        data = json.loads(json_input)
        question = "Answer this question based on given context: " + data['promt'] + " "
        context = " Here is the context: " + str(data['context'])
        question_and_context = question + context

        params = {
            "temperature": float(data['temperature']),
            "max_tokens": int(data['max_tokens'])
        }
        response = llama2_model(prompt=question_and_context, **params)

        answer = response['choices'][0]['text']
        return {"response": answer}
    
    
    except Exception as e:
        print(e)
        return e