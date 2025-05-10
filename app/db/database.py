import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# Load environment variables from .env file
load_dotenv()

# Retrieve Qdrant host and API key from environment variables
QDRANT_HOST = os.getenv("QDRANT_HOST")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "qa90_collection"

# Initialize the Qdrant client
client = QdrantClient(url=QDRANT_HOST, api_key=QDRANT_API_KEY)

def get_qdrant_client():
    return client

def create_collection():
    client = get_qdrant_client()
    
    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,  # Vector dimension for sentence-transformers
                distance=Distance.COSINE  # Use cosine similarity
            )
        )
        print(f"Collection '{COLLECTION_NAME}' created successfully.")
    except Exception as e:
        print(f"Collection creation failed (might already exist): {e}")