import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-1.5-flash"
)

def test_ai():

    response = model.generate_content(
        "Suggest 3 tourist places in Goa"
    )

    return response.text