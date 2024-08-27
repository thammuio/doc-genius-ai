import os

def get_settings_data():
    kb_vector_index = os.getenv('KB_VECTOR_INDEX', 'retail_kb')

    sample_questions_map = {
        'retail_kb': ["What is the Return Policy?", "How long does shipping take?", "What are the shipping options?"],
        'transport_kb': ["What is the current route for truck #12345?", "Do I need to complete any specific forms after a vehicle inspection?", "Can you suggest an alternative route to avoid the road closure on Highway 50?"],
        'itsystems_kb': ["How can I reset my corporate email password?", "What are the steps to connect to the company VPN on a new device?", "Can you guide me through the process of submitting a help desk ticket for a hardware issue?"]
    }

    sample_3_questions = sample_questions_map.get(kb_vector_index, sample_questions_map['retail_kb'])

    return {
        "temperature": 0.7,
        "max_tokens": 100,
        "vector_dbs": [
            {
                "name": "MILVUS",
                "link": "https://milvus.io/"
            },
            {
                "name": "CHROMA",
                "link": "https://www.trychroma.com/"
            },
            {
                "name": "PINECONE",
                "link": "https://www.pinecone.io/"
            },
            {
                "name": "FAISS",
                "link": "https://github.com/facebookresearch/faiss"
            },
            {
                "name": "PGVECTOR",
                "link": "https://github.com/pgvector/pgvector"
            }
        ],
        "user_id": "genius",
        "models": [
            {
                "name": "openai-gpt-4o",
                "link": "https://openai.com/index/gpt-4-research/"
            },
            {
                "name": "llama2-7B-chat",
                "link": "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
            },
            {
                "name": "llama2-13B-chat",
                "link": "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF"
            },
            {
                "name": "Llama-2-7b-chat-hf",
                "link": "https://huggingface.co/NousResearch/Llama-2-7b-chat-hf"
            },
            {
                "name": "Mistral-7B-Instruct",
                "link": "https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2"
            },
            {
                "name": "zephyr-7B-alpha",
                "link": "https://huggingface.co/HuggingFaceH4/zephyr-7b-alpha"
            },
            {
                "name": "Meta-Llama-3-8B-Instruct",
                "link": "https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct"
            },
            {
                "name": "Gemma-7b",
                "link": "https://huggingface.co/google/gemma-7b"
            },
            {
                "name": "Phi-2",
                "link": "https://huggingface.co/microsoft/phi-2"
            },
            {
                "name": "Phi-3-mini-4k-instruct-gguf",
                "link": "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf"
            },
            {
                "name": "OpenELM-3B",
                "link": "https://huggingface.co/apple/OpenELM"
            },            
            {
                "name": "DistilBERT-base",
                "link": "https://huggingface.co/distilbert-base-uncased"
            }
        ],
        "sample_3_questions": sample_3_questions,
        "kb_name": kb_vector_index
    }
