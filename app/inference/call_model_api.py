from openai import OpenAI
import subprocess
import json
import utils.iam


ENDPOINT_URL = os.environ["MODEL_ENDPOINT_URL_1"]
MODEL = os.environ["MODEL_ENDPOINT_ID_1"]
API_KEY = get_model_api_key()

client = OpenAI(
     base_url=ENDPOINT_URL,
     api_key=API_KEY
)

def generate_response(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content": assistant})
    history_openai_format.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(model=MODEL,
                                                  messages=history_openai_format,
                                                  temperature=1.0,
                                                  max_tokens=500,
                                                  stream=True)

        partial_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                partial_message = partial_message + chunk.choices[0].delta.content
                yield partial_message
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")



def generate_response(message, history):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})
  
    response = client.chat.completions.create(model=MODEL,
    messages= history_openai_format,
    temperature=1.0,
    max_tokens=500,
    stream=True)

    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
              partial_message = partial_message + chunk.choices[0].delta.content
              yield partial_message