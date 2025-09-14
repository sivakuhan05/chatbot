# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot import GeminiChatbot
from dotenv import load_dotenv
import os
from typing import Optional, Dict
from langchain.memory import ConversationBufferMemory

# Load variables from .env file
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in .env file.")

chatbot = GeminiChatbot(api_key=API_KEY)

app = FastAPI()

# In-memory mapping of session_id -> ConversationBufferMemory
# This keeps memory only while the process is running.
memory_store: Dict[str, ConversationBufferMemory] = {}

class ChatRequest(BaseModel):
    message: str
    # Optional session id. If omitted, "default" session is used.
    session_id: Optional[str] = None

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or "default"

    try:
        # Create memory for this session if it doesn't exist
        if session_id not in memory_store:
            # default ConversationBufferMemory keeps a simple text buffer
            memory_store[session_id] = ConversationBufferMemory()

        memory = memory_store[session_id]

        # Load the existing history (string) from memory
        memory_history = memory.load_memory_variables({}).get("history", "")

        # Construct a prompt that includes the previous conversation
        # followed by the new user message.
        # (You can change prompt formatting as desired.)
        if memory_history:
            prompt = f"{memory_history}\nUser: {request.message}\nAssistant:"
        else:
            prompt = f"User: {request.message}\nAssistant:"

        # Get response from Gemini via your chatbot wrapper
        reply = chatbot.get_response(prompt)

        # Save user message and model reply into memory for this session
        memory.save_context({"input": request.message}, {"output": reply})

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
