from langchain_openai import AzureChatOpenAI
from db.database import get_qdrant_client
from util.helper import text_to_vector
import os
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, APIRouter

# Load environment variables for LLM
load_dotenv()

# initializing the LLM the azure-ai
endpoint = os.getenv("endpoint")
api_key = os.getenv("api_key")
azure_deployment = os.getenv("azure_deployment")
api_version = os.getenv("api_version")

llm = AzureChatOpenAI(
    api_version=api_version,
    api_key=api_key,
    azure_endpoint=endpoint,
    azure_deployment=azure_deployment
)

app = FastAPI()
router = APIRouter()

COLLECTION_NAME = "qa9_collection"

@router.websocket("/ws/chat/")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            user_message = await websocket.receive_text() # receive the user query

            qdrant_client = get_qdrant_client()
            query_vector = text_to_vector(user_message)

            try:
                search_results = qdrant_client.search(
                    collection_name=COLLECTION_NAME,
                    query_vector=query_vector,
                    limit=3
                )
                if search_results:
                    print(f"Found {len(search_results)} relevant results in Qdrant.")
                else:
                    print("No relevant results found in Qdrant.")
            except Exception as e:
                await websocket.send_text(f"Error searching Qdrant: {str(e)}")
                continue

            # context is the related searches from the qdrant
            context = ""
            for item in search_results:
                question = item.payload.get("question", "No question found.")
                answer = item.payload.get("answer", "No answer found.")
                context += f"Q: {question}\nA: {answer}\n\n"

            # If no relevant search results found, inform the user
            if not context:
                context = "Find from web"

            # prompt for the LLM to generate a result
            prompt = f"Context:\n{context}\n\nUser Query: {user_message}\n\nResponse:"

            # call for the LLM to generate the response according to the requested prompt
            try:
                llm_response = llm.invoke(prompt)
                response = llm_response.content  # Extract response content
                print(f"LLM Response: {response}")
            except Exception as e:
                response = f"Error generating response from LLM: {str(e)}"
                print(f"Error generating LLM response: {str(e)}")

            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("Client disconnected")