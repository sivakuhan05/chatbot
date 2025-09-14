# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import GeminiChatbot
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file.")

chatbot = GeminiChatbot(api_key=API_KEY)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        reply = chatbot.get_response(request.message)
        return {"response": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
