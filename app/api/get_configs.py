def get_settings_data():
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
                "link": ""
            },
            {
                "name": "PINECONE",
                "link": ""
            },
            {
                "name": "FAISS",
                "link": ""
            },
            {
                "name": "PGVECTOR",
                "link": ""
            }
        ],
        "user_id": "genius",
        "models": [
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
                "name": "GPT-4-Turbo",
                "link": "https://huggingface.co/mistralai/Mixtral-8x7B-v0.1"
            },
            {
                "name": "DistilBERT-base",
                "link": "https://huggingface.co/distilbert-base-uncased"
            }
        ]
    }
