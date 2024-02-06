import os
import subprocess

# Get the branch name from the environment variable
branch_name = os.getenv('PROJECT_GIT_BRANCH')

# Check if the branch name is not None
if branch_name:
    # Execute the git checkout command
    subprocess.run(['git', 'checkout', branch_name], check=True)
    
    # Get the current branch name
    current_branch = subprocess.check_output(['git', 'branch']).decode('utf-8')
    print(f"Current branch: {current_branch}")
else:
    print("Environment variable PROJECT_GIT_BRANCH is not set.")