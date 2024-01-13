import os
import json
import cmlapi


CDSW_DOMAIN = os.environ["CDSW_DOMAIN"]
CDSW_APIV2_KEY = os.environ["CDSW_APIV2_KEY"]
CDSW_PROJECT_ID = os.environ["CDSW_PROJECT_ID"]
HEADERS = {'Content-Type': 'application/json'}
MODEL_API_URL = f'https://modelservice.{CDSW_DOMAIN}/model'
WORKSPACE_DOMAIN = f"https://{CDSW_DOMAIN}"
CML_CLIENT = cmlapi.default_client(WORKSPACE_DOMAIN, CDSW_APIV2_KEY)

def get_model_access_key(model_search_string):
    model_to_call = CML_CLIENT.list_models(CDSW_PROJECT_ID, search_filter=json.dumps(model_search_string))
    MODEL_ACCESS_KEY = model_to_call.models[0].access_key 

    return MODEL_ACCESS_KEY
