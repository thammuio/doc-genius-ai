import subprocess

# Define the shell script path
setup_build_script_path = 'chat-ui/setup_build.sh'

# Use subprocess to run the shell script
subprocess.run(['bash', setup_build_script_path], check=True)