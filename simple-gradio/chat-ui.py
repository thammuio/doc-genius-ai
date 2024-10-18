import gradio as gr

import asyncio, httpx
import async_timeout

from loguru import logger
from typing import Optional, List
from pydantic import BaseModel

import os
from dotenv import load_dotenv
load_dotenv()

MODEL_API_KEY = os.getenv("MODEL_API_KEY")
MODEL_API_URL = os.getenv("MODEL_API_URL")
MODEL_NAME = os.getenv("MODEL_NAME")

class Message(BaseModel):
    role: str
    content: str

async def make_completion(messages:List[Message], nb_retries:int=3, delay:int=30) -> Optional[str]:
    """
    Sends a request to the AI Inference API to retrieve a response based on a list of previous messages.
    """
    header = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MODEL_API_KEY}"
    }
    try:
        async with async_timeout.timeout(delay=delay):
            async with httpx.AsyncClient(headers=header) as aio_client:
                counter = 0
                keep_loop = True
                while keep_loop:
                    logger.debug(f"Chat/Completions Nb Retries : {counter}")
                    try:
                        resp = await aio_client.post(
                            url = f"{MODEL_API_URL}",
                            json = {
                                "model": f"{MODEL_NAME}",
                                "messages": messages
                            }
                        )
                        logger.debug(f"Status Code : {resp.status_code}")
                        if resp.status_code == 200:
                            return resp.json()["choices"][0]["message"]["content"]
                        else:
                            logger.warning(resp.content)
                            keep_loop = False
                    except Exception as e:
                        logger.error(e)
                        counter = counter + 1
                        keep_loop = counter < nb_retries
    except asyncio.TimeoutError as e:
        logger.error(f"Timeout {delay} seconds !")
    return None

async def predict(input, history):
    """
    Predict the response of the chatbot and complete a running list of chat history.
    """
    history.append({"role": "user", "content": input})
    response = await make_completion(history)
    history.append({"role": "assistant", "content": response})
    messages = [(history[i]["content"], history[i+1]["content"]) for i in range(0, len(history)-1, 2)]
    return messages, history


"""
Define Theme for the Chatbot
"""

theme = gr.themes.Base()




"""
Gradio Blocks low-level API that allows to create custom web applications (here our chat app)
"""

with gr.Blocks(
    title="SimpleGeniusUI",
    theme=theme,
) as demo:
    logger.info("Starting Chatbot...")

    # Add navigation header
    gr.Markdown("""
    # SimpleGeniusUI
    """)

    # Add header
    gr.Markdown("## Chat Interface")

    chatbot = gr.Chatbot(label="SimpleGeniusUI")
    state = gr.State([])
    # Move the textbox to the bottom
    with gr.Row():
        txt = gr.Textbox(show_label=False, placeholder="Enter text and press enter", container=False)
    txt.submit(predict, [txt, state], [chatbot, state])



demo.launch(server_port=8080, show_api=False)


# demo.launch(server_port=8080, share=True)