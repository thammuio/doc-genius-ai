import subprocess

# Define the shell script path
deploy_script_path = 'chat-ui/deploy.sh'

# Use subprocess to run the shell script
subprocess.run(['bash', deploy_script_path], check=True)