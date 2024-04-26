import subprocess
import sys

# Define the command to be executed
command = [sys.executable, "-m", "pip", "install", "--no-cache-dir", "-r", "session/install-deps/requirements.txt"]

try:
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True, check=True)

    # Print the output
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    # Handle errors in the subprocess
    print("Error:", e.stderr)
    sys.exit(e.returncode)
