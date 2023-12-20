import os
import subprocess

# Change the current working directory to 'chat-ui'
os.chdir('chat-ui')

# Set the HOST and PORT environment variables
os.environ['HOST'] = '127.0.0.1'
os.environ['PORT'] = '8080'

# Run the 'yarn start' command in the background
process = subprocess.Popen(["yarn", "start"])

# Return a success code
exit_code = process.poll()
if exit_code is None:
    print("Process is running in the background successfully.")
else:
    print(f"Process failed with exit code {exit_code}")