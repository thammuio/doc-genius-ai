
# Send Requests to LLMs
POST /chat

```json
{
    "prompt": "What is Cloudera Machine Learning?",
    "parameters": {
        "temperature": 1,
        "max_tokens": 10
    },
    "selected_model": "poc/gpu/rag/llama-2-13b-chat",
    "selected_vector_db": "MILVUS",
    "user": "genius"
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
    "temperature": 1,
    "max_tokens": 100,
    "models": [
        {
            "name": "poc/gpu/rag/llama-2-7b-chat",
            "link": "https://huggingface.co/meta-llama/Llama-2-7b-chat-hf"
        },
        {
            "name": "gpu/rag/llama-2-7b-chat",
            "link": "https://huggingface.co/meta-llama/Llama-2-7b-chat-hf"
        },
        {
            "name": "gpu/prompt/Mixtral-8x7B",
            "link": "https://huggingface.co/mistralai/Mixtral-8x7B-v0.1"
        },
        {
            "name": "gpu/fine-tuned/Mixtral-8x7B",
            "link": "https://huggingface.co/mistralai/Mixtral-8x7B-v0.1"
        },
        {
            "name": "cpu/rag/distilbert-base-uncased",
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