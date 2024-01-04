# Define Model flow based on Selection

def get_model_variables(model_name):
    if model_name == "llama-2-13b-chat":
        ENGINE_NAME = "llama-2-13b-chat"
        GEN_AI_MODEL_REPO = "TheBloke/Llama-2-13B-chat-GGUF"
        GEN_AI_MODEL_FILENAME = "llama-2-13b-chat.Q5_0.gguf"
        EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"
    elif model_name == "llama-2-70b-chat":
        # Set the variables for the llama-2-70b-chat model
        ENGINE_NAME = "llama-2-70b-chat"
        GEN_AI_MODEL_REPO = "TheBloke/Llama-2-70B-chat-GGUF"  # Replace with actual repo
        GEN_AI_MODEL_FILENAME = "llama-2-70b-chat.Q5_0.gguf"  # Replace with actual filename
        EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"  # Replace with actual repo
    elif model_name == "llama-2-7b-chat":
        # Set the variables for the llama-2-7b-chat model
        ENGINE_NAME = "llama-2-7b-chat"
        GEN_AI_MODEL_REPO = "TheBloke/Llama-2-7B-chat-GGUF"  # Replace with actual repo
        GEN_AI_MODEL_FILENAME = "llama-2-7b-chat.Q5_0.gguf"  # Replace with actual filename
        EMBEDDING_MODEL_REPO = "sentence-transformers/all-mpnet-base-v2"  # Replace with actual repo
    else:
        raise ValueError(f"Unsupported model: {model_name}")

    return ENGINE_NAME, GEN_AI_MODEL_REPO, GEN_AI_MODEL_FILENAME, EMBEDDING_MODEL_REPO
# Usage
ENGINE_NAME, GEN_AI_MODEL_REPO, GEN_AI_MODEL_FILENAME, EMBEDDING_MODEL_REPO = get_model_variables("llama-2-13b-chat")