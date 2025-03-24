from fastapi import FastAPI
from api.routes import search, upload, chatbot
from fastapi import WebSocket
import uvicorn

app =FastAPI()

app.include_router(upload.router)
app.include_router(chatbot.router)
# app.include_router(search.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)   