from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import warnings
warnings.filterwarnings("ignore")
import json
import os


# Define the model 
GEN_AI_MODEL_REPO = "TheBloke/Llama-2-13B-chat-GGUF"
GEN_AI_MODEL_FILENAME = "llama-2-13b-chat.Q2_K.gguf"

print("Initiate Llama model...")
def load_llama_model():
    gen_ai_model_path = hf_hub_download(repo_id=GEN_AI_MODEL_REPO, filename=GEN_AI_MODEL_FILENAME)
    print("path is:")
    print(gen_ai_model_path)
    llama2_model = Llama(
        model_path=gen_ai_model_path,
        n_gpu_layers=64,
        n_ctx=2000
    )
    return llama2_model


llama2_model = load_llama_model()

print("Model loaded successfully!")

# Pass through user input to LLM model with enhanced prompt and stop tokens
def generate_response(json_input):
    try:
        question = "Answer this question based on given context: " + json_input['prompt'] + " "
        context = " Here is the context: " + str(json_input['context'])
        question_and_context = question + context

        params = {
            "temperature": float(json_input['temperature']),
            "max_tokens": int(json_input['max_tokens'])
        }
        response = llama2_model(prompt=question_and_context, **params)

        model_out = response['choices'][0]['text']

        # Return a serializable object
        return {"response": model_out}
    
    except KeyError as ke:
        print(f"KeyError: {ke}")
        return {"error": f"Missing key: {ke}"}
    except Exception as e:
        print(str(e))
        return {"error": str(e)}  # Use str(e) to ensure the error message is serializable
