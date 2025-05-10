# from fastapi import FastAPI, APIRouter
# from qdrant_client.models import Filter, SearchRequest
# from db.database import get_qdrant_client
# from util.helper import text_to_vector

# router = APIRouter()
# app = FastAPI()
# COLLECTION_NAME = "qa9_collection"

# @router.get("/search/")
# async def search_qna(query: str, top_k: int = 5):

#     qdrant_client = get_qdrant_client()
    
#     # Convert the query to a vector
#     query_vector = text_to_vector(query)

#     try:
#         # Perform search in Qdrant
#         search_results = qdrant_client.search(
#             collection_name=COLLECTION_NAME,
#             query_vector=query_vector,
#             limit=top_k  # Retrieve top_k most relevant results
#         )

#         # Extract and format results
#         results = [
#             {
#                 "question": i.payload["question"],
#                 "answer": i.payload["answer"]
#             }
#             for i in search_results
#         ]

#         return {"matches": results}
    
#     except Exception as e:
#         return {"message": f"Error searching Qdrant: {e}"}

from qdrant_client import QdrantClient
from util.helper import text_to_vector

# Initialize Qdrant client
qdrant_client = QdrantClient(url="YOUR_QDRANT_URL", api_key="YOUR_API_KEY")
COLLECTION_NAME = "qa9_collection"

# Reusable function for searching relevant answers
def search_similar_answers(query: str, top_k: int = 5):
    try:
        # Convert the query to a vector
        query_vector = text_to_vector(query)
        
        # Perform the search in Qdrant
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k
        )

        # Format the results and return them
        results = [
            {
                "question": result.payload["question"],
                "answer": result.payload["answer"]
            }
            for result in search_results
        ]

        return results
    except Exception as e:
        raise Exception(f"Error during search in Qdrant: {str(e)}")
