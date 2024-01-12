import os
import json
import cmlapi

ENV_VARS = {
    "domain": "CDSW_DOMAIN",
    "api_key": "CDSW_APIV2_KEY",
    "project_id": "CDSW_PROJECT_ID"
}

MODEL_NAMES_IN_PROJECT_METADATA_YAML = [
    "POC LLM Model",
    "Prompt Enchanced LLM Model",
    "RAG Enchanced LLM Model",
    "Fine-tuning LLM Model"
]

def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise Exception(f"Environment variable {var_name} not found.")

def get_model_access_key(client, project_id, model_name):
    model = client.list_models(project_id, search_filter=json.dumps({"name": model_name}))
    if model.models:
        return model.models[0].access_key
    else:
        raise Exception(f"Model {model_name} not found.")

# below variables does not change overtime and we can persists them in memory
DOMAIN = get_env_var(ENV_VARS["domain"])
API_KEY = get_env_var(ENV_VARS["api_key"])
PROJECT_ID = get_env_var(ENV_VARS["project_id"])
HEADERS = {'Content-Type': 'application/json'}
API_URL = f'https://modelservice.{DOMAIN}/model'
WORKSPACE_DOMAIN = f"https://{DOMAIN}"
CML_CLIENT = cmlapi.default_client(WORKSPACE_DOMAIN, API_KEY)


# Initialize the variables as None
MODEL_ACCESS_KEYS = {
    "POC_MODEL_ACCESS_KEY": None,
    "PROMPT_MODEL_ACCESS_KEY": None,
    "RAG_MODEL_ACCESS_KEY": None,
    "FINETUNING_MODEL_ACCESS_KEY": None
}

# below variables also does not change overtime and we can persists them in memory
# Now you can use the try blocks
for i, model_name in enumerate(MODEL_NAMES_IN_PROJECT_METADATA_YAML):
    key_name = list(MODEL_ACCESS_KEYS.keys())[i]
    try:
        if MODEL_ACCESS_KEYS[key_name] is None:
            MODEL_ACCESS_KEYS[key_name] = get_model_access_key(CML_CLIENT, PROJECT_ID, model_name)
    except NameError:
        MODEL_ACCESS_KEYS[key_name] = get_model_access_key(CML_CLIENT, PROJECT_ID, model_name)