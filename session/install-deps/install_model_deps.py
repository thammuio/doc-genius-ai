import subprocess
import sys

# Define the path to the shell script
llama_deps_script_path = "session/install-deps/install_llama_deps.sh"

try:
    # Run the shell script
    result = subprocess.run(["sh", llama_deps_script_path], capture_output=True, text=True, check=True)

    # Print the output
    print("Output:", result.stdout)
except subprocess.CalledProcessError as e:
    # Handle errors in the subprocess
    print("Error:", e.stderr)
    sys.exit(e.returncode)
