from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import warnings
warnings.filterwarnings("ignore")
import json
import os


# Define the model 
GEN_AI_MODEL_REPO = "TheBloke/Llama-2-13B-chat-GGUF"
GEN_AI_MODEL_FILENAME = "llama-2-13b-chat.Q5_0.gguf"

print("Initiate Llama model...")
def load_llama_model():
    gen_ai_model_path = hf_hub_download(repo_id=GEN_AI_MODEL_REPO, filename=GEN_AI_MODEL_FILENAME)
    print("path is:")
    print(gen_ai_model_path)
    llama2_model = Llama(
        model_path=gen_ai_model_path,
        n_gpu_layers=20,
        n_ctx=20
    )
    return llama2_model


llama2_model = load_llama_model()

print("Model loaded successfully!")

# Pass through user input to LLM model with enhanced prompt and stop tokens
def generate_response(json_input):

    try:
        print("Input from user: ")
        print(json_input)
        # Assuming json_input is your dictionary
        json_input_str = json.dumps(json_input)
        data = json.loads(json_input_str)
        print("json.loads:")
        print(data)
        question = "Answer this question based on given context: " + data['prompt'] + " "
        context = " Here is the context: " + str(data['context'])
        question_and_context = question + context

        params = {
            "temperature": float(data['temperature']),
            "max_tokens": int(data['max_tokens'])
        }
        response = llama2_model(prompt=question_and_context, **params)

        model_out = response['choices'][0]['text']

        print("Response from Llama model: ")
        print(response)
        print("--------------------------- ")
        print(model_out)
        print("--------------------------- ")

        # answer = response['choices'][0]['text']
        return {"response": "Success"}
    
    
    except Exception as e:
        print(e)
        return e
