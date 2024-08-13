import os
import boto3
import pandas as pd
import pinecone
from transformers import AutoTokenizer, AutoModel
import torch
import s3fs

# Pinecone configuration
PINECONE_API_KEY = "e11a8542-532c-47ae-adfa-70c888cfb766"
PINECONE_ENVIRONMENT = "us-east-1"  # Replace with your environment
PINECONE_INDEX_NAME = "mini-lm"  # Replace with your Pinecone index name

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index(PINECONE_INDEX_NAME)

# Initialize S3 filesystem (no auth needed)
s3 = s3fs.S3FileSystem(anon=True)
bucket_path = 's3://pinecone-suri/text/'

# List all CSV files in the S3 bucket directory
csv_files = s3.glob(os.path.join(bucket_path, '*.csv'))

# Initialize the embedding model
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')
model = AutoModel.from_pretrained('sentence-transformers/all-MiniLM-L6-v2')

# Function to create embeddings
def create_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        embeddings = model(**inputs).last_hidden_state.mean(dim=1)
    return embeddings.numpy().flatten()

# Function to read CSV files from S3 and process them
def process_csv_file(file_key):
    with s3.open(file_key, 'rb') as f:
        df = pd.read_csv(f)

    # Iterate over the DataFrame and insert into Pinecone
    for _, row in df.iterrows():
        text = row['Question'] + " " + row['Answer']
        category = row['Category']
        question_id = row['Question ID']
        
        embedding = create_embedding(text)
        
        # Upsert the vector into Pinecone
        index.upsert(vectors=[(question_id, embedding.tolist(), {"category": category})])

# Process all CSV files in the S3 bucket
for file_key in csv_files:
    process_csv_file(file_key)

print("Data inserted into Pinecone successfully!")