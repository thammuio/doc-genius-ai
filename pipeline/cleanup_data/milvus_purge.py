from pymilvus import connections, utility
import os

MILVUS_COLLECTION = os.getenv('MILVUS_COLLECTION')

def delete_milvus_collection(MILVUS_COLLECTION):
    # Connect to the default server
    connections.connect()

    # Check if the collection exists
    if utility.has_collection(MILVUS_COLLECTION):
        # Drop the collection
        utility.drop_collection(MILVUS_COLLECTION)
        print(f"Collection {MILVUS_COLLECTION} has been deleted.")
    else:
        print(f"Collection {MILVUS_COLLECTION} does not exist.")

# Delete the collection
delete_milvus_collection(MILVUS_COLLECTION)