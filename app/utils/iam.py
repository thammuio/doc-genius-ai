import os
import json
import cmlapi
import subprocess


print("Generating CDP API key...")
api_key_process = subprocess.run(
     "cdp iam generate-workload-auth-token --workload-name DE --profile cml_env",
     shell=True,
     capture_output=True
)

def get_model_api_key():
    API_KEY = json.loads(api_key_process.stdout)['token']

    return API_KEY