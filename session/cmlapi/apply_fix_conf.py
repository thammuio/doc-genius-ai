import os
import json
import cmlapi

def get_env_var(var_name):
    try:
        return os.environ[var_name]
    except KeyError:
        raise Exception(f"Environment variable {var_name} not set")

def get_app_id(cml_client, project_id, app_name):
    try:
        app_list = cml_client.list_applications(project_id, search_filter=json.dumps({"name": app_name}))
        return app_list.applications[0].id
    except cmlapi.exceptions.ApiException as e:
        raise Exception(f"API error occurred: {str(e)}")

def update_and_restart_app(cml_client, project_id, app_id, subdomain):
    try:
        cml_client.update_application({"subdomain": subdomain}, project_id, app_id)
        cml_client.restart_application(project_id, app_id)
    except cmlapi.exceptions.ApiException as e:
        raise Exception(f"API error occurred: {str(e)}")

def main():
    CDSW_DOMAIN = get_env_var("CDSW_DOMAIN")
    CDSW_APIV2_KEY = get_env_var("CDSW_APIV2_KEY")
    CDSW_PROJECT_ID = get_env_var("CDSW_PROJECT_ID")

    WORKSPACE_DOMAIN = f"https://{CDSW_DOMAIN}"
    cml_client = cmlapi.default_client(WORKSPACE_DOMAIN, CDSW_APIV2_KEY)

    API_APP_ID = get_app_id(cml_client, CDSW_PROJECT_ID, "API for Chatbot")
    update_and_restart_app(cml_client, CDSW_PROJECT_ID, API_APP_ID, "docgenius-api")

    UI_APP_ID = get_app_id(cml_client, CDSW_PROJECT_ID, "Frontend UI")
    update_and_restart_app(cml_client, CDSW_PROJECT_ID, UI_APP_ID, "docgenius-ui")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        exit(1)