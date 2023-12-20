import subprocess

# Define the shell script path
shell_script_path = 'chat-ui/start.sh'

# Use subprocess to run the shell script
subprocess.run(['bash', shell_script_path], check=True)