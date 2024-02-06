import pinecone

def init_pinecone(api_key, environment, index_name):
    print("initialising Pinecone connection...")
    pinecone.init(api_key=api_key, environment=environment)
    print("Pinecone initialised")

    print(f"Getting '{index_name}' as object...")
    index = pinecone.Index(index_name)
    print("Success")

    # Get latest statistics from index
    current_collection_stats = index.describe_index_stats()
    print('Total number of embeddings in Pinecone index is {}.'.format(current_collection_stats.get('total_vector_count')))

    return index
