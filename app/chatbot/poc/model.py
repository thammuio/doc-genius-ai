from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pydantic import BaseModel
from typing import Any, Union, Optional
from app.embeddings.chunk_utils import *
import warnings
warnings.filterwarnings("ignore")
import json

# Define the model 
GEN_AI_MODEL_REPO = "TheBloke/Llama-2-13B-chat-GGUF"
GEN_AI_MODEL_FILENAME = "llama-2-13b-chat.Q5_0.gguf"

# Download and Load model from HuggingFace Hub
print("Downloading model from HuggingFace Hub...")
gen_ai_model_path = hf_hub_download(repo_id=GEN_AI_MODEL_REPO, filename=GEN_AI_MODEL_FILENAME)

print("Initiate Llama model...")
llama2_model = Llama(
    model_path=gen_ai_model_path,
    n_gpu_layers=64,
    n_ctx=2000
)

print("Model loaded successfully!")

# Pass through user input to LLM model with enhanced prompt and stop tokens
def generate_response(json_input):

    try:
        data = json.loads(json_input)
        print(data)
        question = "Answer this question based on given context: " + data['prompt'] + " "
        context = " Here is the context: " + str(data['context'])
        question_and_context = question + context

        params = {
            "temperature": float(data['temperature']),
            "max_tokens": int(data['max_tokens'])
        }
        response = llama2_model(prompt=question_and_context, **params)

        print("Response from Llama model: ")
        print("--------------------------- ")
        print(response)
        print("--------------------------- ")

        # answer = response['choices'][0]['text']
        return {"response": "Success"}
    
    
    except Exception as e:
        print(e)
        return e