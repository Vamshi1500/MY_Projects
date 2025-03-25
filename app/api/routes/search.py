from fastapi import FastAPI, APIRouter
from qdrant_client.models import Filter, SearchRequest
from db.database import get_qdrant_client
from util.helper import text_to_vector

router = APIRouter()
app = FastAPI()
COLLECTION_NAME = "qa9_collection"

@router.get("/search/")
async def search_qna(query: str, top_k: int = 5):

    qdrant_client = get_qdrant_client()
    
    # Converting the query to a vector
    query_vector = text_to_vector(query)

    try:
        # Perform search in Qdrant
        search_results = qdrant_client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=top_k  # most relavent question and answers
        )

        # Extract and formating the results
        results = [
            {
                "question": i.payload["question"],
                "answer": i.payload["answer"]
            }
            for i in search_results
        ]

        return {"matches": results}
    
    except Exception as e:
        return {"message": f"Error searching Qdrant: {e}"}