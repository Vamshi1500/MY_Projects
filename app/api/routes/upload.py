from fastapi import FastAPI, UploadFile, File, APIRouter
import shutil
import os
from api.routes.doc_processing import extract_questions_and_answers
from util.helper import model, text_to_vector
from db.database import get_qdrant_client, client
import numpy as np
from qdrant_client.models import PointStruct

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure the upload directory exists

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    # Save the uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    questions, answers = extract_questions_and_answers(file_path)
    
    qdrant_client = get_qdrant_client()

    points = []
    for i, (question, answer) in enumerate(zip(questions, answers)):
        # Convert both question and answer to vectors
        question_vector = text_to_vector(question)
        answer_vector = text_to_vector(answer)

        # Combine question and answer vector (or you could just use one of them)
        combined_vector = np.mean([question_vector, answer_vector], axis=0).tolist()

        # Create a PointStruct for each pair (with a unique ID)
        point = PointStruct(
            id=i + 1,  # Unique ID for each QA pair
            vector=combined_vector,  # Combined vector for question and answer
            payload={"question": question, "answer": answer}  # Metadata: question and answer
        )
        points.append(point)
    
    try:
        # Upsert the points into Qdrant collection
        client.upsert(collection_name="qa9_collection", points=points)
        return {"message":f"Successfully inserted {len(points)} question-answer pairs into Qdrant."}
    except Exception as e:
        return {"message":f"Error upserting into Qdrant: {e}"}