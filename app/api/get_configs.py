def get_settings_data():
    return {
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