def get_settings_data():
    return {
        "temperature": 1,
        "max_tokens": 100,
        "models": [
            {
                "name": "poc/gpu/rag/llama-2-3b-chat",
                "link": "https://huggingface.co/meta-llama/Llama-2-13b-chat-hf"
            },
            {
                "name": "gpu/rag/llama-2-13b-chat",
                "link": "https://huggingface.co/meta-llama/Llama-2-13b-chat-hf"
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