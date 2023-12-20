import os
import subprocess

# Change the current working directory to 'chat-ui'
os.chdir('chat-ui')

# Run the 'yarn build' command
subprocess.run(["yarn", "build"], check=True)