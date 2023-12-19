import os
import subprocess
import app.embeddings.embeddings_utils as model_embedding
from pathlib import Path
import pinecone
from sentence_transformers import SentenceTransformer

VECTOR_DB = os.getenv('VECTOR_DB').upper()
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT')
PINECONE_INDEX = os.getenv('PINECONE_INDEX')
dimension = 768

def create_pinecone_collection(PINECONE_INDEX):
    try:
        print(f"Creating 768-dimensional index called '{PINECONE_INDEX}'...")
        pinecone.create_index(PINECONE_INDEX, dimension=768)
        print("Success")
    except:
        # index already created, continue
        pass

    print("Checking Pinecone for active indexes...")
    active_indexes = pinecone.list_indexes()
    print("Active indexes:")
    print(active_indexes)
    print(f"Getting description for '{PINECONE_INDEX}'...")
    index_description = pinecone.describe_index(PINECONE_INDEX)
    print("Description:")
    print(index_description)

    print(f"Getting '{PINECONE_INDEX}' as object...")
    pinecone_index = pinecone.Index(PINECONE_INDEX)
    print("Success")
    
    return pinecone_index
    
    
# Create an embedding for given text/doc and insert it into Pinecone Vector DB
def insert_embedding(pinecone_index, id_path, text):
    print("Upserting vectors...")
    vectors = list(zip([text[:512]], [model_embedding.get_embeddings(text)], [{"file_path": id_path}]))
    upsert_response = pinecone_index.upsert(
        vectors=vectors
        )
    print("Success")
    
    
def main():
    if os.getenv('VECTOR_DB').upper() == "PINECONE":
        try:
            print("initialising Pinecone connection...")
            pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
            print("Pinecone initialised")
            
            collection = create_pinecone_collection(PINECONE_INDEX)
            
            # Same files are ignored (e.g. running process repetitively won't overwrite, just pick up new files)
            print("Pinecone index is up and collection is created")

            # Read KB documents in ./data directory and insert embeddings into Vector DB for each doc
            doc_dir = './data'
            for file in Path(doc_dir).glob(f'**/*.txt'):
                with open(file, "r") as f: # Open file in read mode
                    print("Generating embeddings for: %s" % file.name)
                    text = f.read()
                    insert_embedding(collection, os.path.abspath(file), text)
            print('Finished loading Knowledge Base embeddings into Pinecone')

        except Exception as e:
            raise (e)


if __name__ == "__main__":
    main()
