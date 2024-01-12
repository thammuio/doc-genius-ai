from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from pydantic import BaseModel
from typing import Any, Union, Optional
from app.embeddings.chunk_utils import *
import warnings
warnings.filterwarnings("ignore")
import json
from app.utils.constants import GEN_AI_MODEL_REPO, GEN_AI_MODEL_FILENAME


# Pass through user input to LLM model with enhanced prompt and stop tokens
def generate_response(json_input):
    print("Downloading model from HuggingFace Hub...1")
    gen_ai_model_path = hf_hub_download(repo_id=GEN_AI_MODEL_REPO, filename=GEN_AI_MODEL_FILENAME)

    print("Initiate Llama model...")
    llama2_model = Llama(
        model_path=gen_ai_model_path,
        n_gpu_layers=64,
        n_ctx=2000
    )

    try:
        data = json.loads(json_input)
        question = "Answer this question based on given context: " + data['prompt'] + " "
        context = " Here is the context: " + str(data['context'])
        question_and_context = question + context

        params = {
            "temperature": float(data['temperature']),
            "max_tokens": int(data['max_tokens'])
        }
        response = llama2_model(prompt=question_and_context, **params)

        answer = response['choices'][0]['text']
        return {"answer": answer}
    
    
    except Exception as e:
        print(e)
        return e