# chatbot.py
import os
from google import genai
from google.genai import types

class GeminiChatbot:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def get_response(self, user_message: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[user_message]
            )

            # Safely extract the text from response
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "⚠️ No response from Gemini model."

        except Exception as e:
            return f"Error: {str(e)}"
