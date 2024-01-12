from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from app.utils.constants import GEN_AI_MODEL_REPO, GEN_AI_MODEL_FILENAME

def load_llama_model():
    gen_ai_model_path = hf_hub_download(repo_id=GEN_AI_MODEL_REPO, filename=GEN_AI_MODEL_FILENAME)

    llama2_model = Llama(
        model_path=gen_ai_model_path,
        n_gpu_layers=64,
        n_ctx=2000
    )

    return llama2_model