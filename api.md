
# Send Requests to LLMs
POST /chat

```json
{
    "prompt": "What is Cloudera Machine Learning?",
    "parameters": {
        "temperature": 1,
        "max_tokens": 10,
        "model": "llama-2-13b-chat"
    }
}
```


```json
{
    "response": " Cloudera Machine Learning empowers you"
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
            "name": "llama-2-13b-chat",
            "link": "https://huggingface.co/meta-llama/Llama-2-13b-chat-hf"
        },
        {
            "name": "llama-2-70b-chat",
            "link": "https://huggingface.co/meta-llama/Llama-2-70b-chat-hf"
        },
        {
            "name": "llama-2-7b-chat",
            "link": "https://huggingface.co/meta-llama/Llama-2-7b-chat-hf"
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
    "inputs": "What is Cloudera Machine Learning?",
    "temperature": 1,
    "max_tokens": 10,
    "context": "Cloudera Docs"
}