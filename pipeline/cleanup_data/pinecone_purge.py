import os
import pinecone

PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY)

def delete_pinecone_index(PINECONE_INDEX):
    # Check if the index exists
    if PINECONE_INDEX in pinecone.list_indexes():
        # Delete the index
        pinecone.deinit_index(PINECONE_INDEX)
        print(f"Index {PINECONE_INDEX} has been deleted.")
    else:
        print(f"Index {PINECONE_INDEX} does not exist.")

# Delete the index
delete_pinecone_index(PINECONE_INDEX)

# Deinitialize Pinecone
pinecone.deinit()