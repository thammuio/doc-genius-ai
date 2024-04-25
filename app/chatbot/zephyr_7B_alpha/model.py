import os
import shutil
import time
import warnings
warnings.filterwarnings("ignore")
import textwrap
import langchain
import torch
import transformers
from langchain.llms import HuggingFacePipeline
from langchain.chains import LLMChain
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
from langchain.prompts import PromptTemplate
from huggingface_hub import login

hugging_face_model = "HuggingFaceH4/zephyr-7b-alpha"
access_token = os.environ["HF_TOKEN"]
if access_token:
    login(token=access_token)

tokenizer = AutoTokenizer.from_pretrained(hugging_face_model)

llm_model = AutoModelForCausalLM.from_pretrained(hugging_face_model,
                                                     load_in_4bit=True,
                                                     device_map='auto',
                                                     torch_dtype=torch.float16,
                                                     low_cpu_mem_usage=True
                                                    )
max_len = 8192
llm_task = "text-generation"
#llm_task = "text-generation"
T = 0.1

llm_pipeline = pipeline(
    task=llm_task,
    model=llm_model, 
    tokenizer=tokenizer, 
    max_length=max_len,
    temperature=T,
    top_p=0.95,
    repetition_penalty=1.15
)

text_llm = HuggingFacePipeline(pipeline=llm_pipeline)

# Prompt Template for Langchain
template = """You are a helpful AI assistant, answer the below question in detail.
Question:{question}
>>Answer<<"""
prompt_template = PromptTemplate(input_variables=["question"], template = template)


text_chain = LLMChain(llm=text_llm, prompt=prompt_template)

def generate_response(question):
    sum_text = text_chain(question)
    
    return sum_text["text"]