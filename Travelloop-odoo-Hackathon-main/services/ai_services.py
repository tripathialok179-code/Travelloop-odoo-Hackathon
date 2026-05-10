import os
import json

import google.generativeai as genai

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Initialize Gemini model
model = genai.GenerativeModel(
    "gemini-1.5-flash"
)


# -------------------------------
# TEST AI CONNECTION
# -------------------------------
def test_ai():

    response = model.generate_content(
        "Suggest 3 tourist places in Goa"
    )

    return response.text


# -------------------------------
# GENERATE AI TRIP PLAN
# -------------------------------
def generate_trip_plan(data):

    budget = data.get("budget")

    days = data.get("days")

    interests = data.get("interests")

    prompt = f"""
    Create a detailed India travel itinerary.

    Budget: ₹{budget}

    Days: {days}

    Interests: {interests}

    Return:
    - Best cities to visit
    - Day-wise itinerary
    - Activities
    - Food recommendations
    - Estimated costs
    - Transport suggestions

    Format the response properly.
    """

    response = model.generate_content(
        prompt
    )

    return response.text