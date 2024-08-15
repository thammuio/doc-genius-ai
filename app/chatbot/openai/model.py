import requests

def chat_completion(api_key, model, messages, knowledge_base):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # Add knowledge base to the messages
    messages.insert(1, {"role": "system", "content": f"Knowledge Base: \n{knowledge_base}"})
    
    payload = {
        "model": model,
        "messages": messages
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}