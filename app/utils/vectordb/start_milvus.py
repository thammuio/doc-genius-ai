from milvus import default_server
from pymilvus import connections, utility
import time
import os

# Initialize variables
timeout_millis = 120000  # 2 minutes timeout
check_interval_millis = 100  # 100 ms between each check
elapsed_time_millis = 0

kb_name = os.getenv('KB_VECTOR_INDEX')
new_base_dir = f"milvus-data-{kb_name}"
# Start Milvus Vector DB
default_server.stop()
default_server.set_base_dir(new_base_dir)

while elapsed_time_millis < timeout_millis:
    try:
        # Try starting the server
        default_server.start()
        # Try connecting
        connections.connect(alias='default', host='localhost', port=default_server.listen_port)
        print("Successfully connected!")
        print(utility.get_server_version())
        break
    except Exception as e:
        print(f"An error occurred: {e}")
        # Stop the server if it's running
        default_server.stop()
        # Wait before retrying
        time.sleep(check_interval_millis / 1000.0)
        elapsed_time_millis += check_interval_millis

if elapsed_time_millis >= timeout_millis:
    print(f"Timeout: Unable to start and connect to Milvus server in {timeout_millis} milliseconds.")
