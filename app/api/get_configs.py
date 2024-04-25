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
                "name": "zephyr-7b-alpha",
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
