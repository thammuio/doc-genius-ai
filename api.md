
# Send Requests to LLMs
POST /chat

```json
{
    "prompt": "What is Cloudera Machine Learning?",
    "temperature": 1,
    "max_tokens": 10,
    "model": "llama-2-13b-chat",
    "vector_db": "MILVUS",
    "user_id": "genius"
}
```


```json
{
    "answer": "Cloudera Machine Learning empowers you"
}
```

# Get Available Modles and Settings
GET /settings

```json
{
        "temperature": 0.7,
        "max_tokens": 100,
        "vector_dbs": ["MILVUS", "CHROMA", "PINECONE", "FAISS", "PGVECTOR"],
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
```

# Get App Status
GET /status

```json
{
    "api_status": "Healthy",
    "gpu_status": "Available"
}
```

# Model Serving

{
    "prompt": "What is Cloudera Machine Learning?",
    "temperature": 1,
    "max_tokens": 200,
    "context": "Cloudera Machine Learning is a platform for machine learning and analytics that runs in the public cloud or on-premises.",
    "user": "genius"
}

--
{
    "answer": "Cloudera Machine Learning empowers you"
}