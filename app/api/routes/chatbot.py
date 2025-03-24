# from fastapi import APIRouter
# from db.database import get_qdrant_client
# from util.helper import text_to_vector

# router = APIRouter()
# COLLECTION_NAME = "qa9_collection"  # Ensure this matches your collection name

# @router.post("/chat/")
# async def chat_with_bot(user_message: str, top_k: int = 3):
#     qdrant_client = get_qdrant_client()

#     # Convert the user message to a vector
#     user_message_vector = text_to_vector(user_message)

#     try:
#         # Perform search in Qdrant to find the most relevant questions and answers
#         search_results = qdrant_client.search(
#             collection_name=COLLECTION_NAME,
#             query_vector=user_message_vector,
#             limit=top_k  # Return top_k most relevant results
#         )

#         # Extract the results and get the most relevant answers
#         results = []
#         for item in search_results:
#             results.append({
#                 "question": item.payload["question"],
#                 "answer": item.payload["answer"]
#             })

#         if results:
#             return {"bot_response": results}
#         else:
#             return {"bot_response": "Sorry, I couldn't find an answer to that."}

#     except Exception as e:
#         return {"message": f"Error: {e}"}

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from db.database import get_qdrant_client
from util.helper import text_to_vector
import json

router = APIRouter()
COLLECTION_NAME = "qa9_collection"

@router.websocket("/chat/")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            user_message = await websocket.receive_text()
            
            user_message_vector = text_to_vector(user_message)
            
            qdrant_client = get_qdrant_client()

            search_results = qdrant_client.search(
                collection_name=COLLECTION_NAME,
                query_vector=user_message_vector,
                limit=3
            )
            
            response = ""
            if search_results:
                # Format the results as plain text
                for item in search_results:
                    question = item.payload["question"]
                    answer = item.payload["answer"]
                    response += f"Question: {question}\nAnswer: {answer}\n\n"
            else:
                response = {
                    "bot_response": "Answer not found."
                }

            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("Client disconnected")