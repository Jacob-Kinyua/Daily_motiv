from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, json

load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_json(prompt, schema):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=schema,
        )
    )

    return response.parsed