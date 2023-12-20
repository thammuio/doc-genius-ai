import subprocess

# Define the shell script path
setup_script_path = 'chat-ui/setup.sh'

# Use subprocess to run the shell script
subprocess.run(['bash', setup_script_path], check=True)