from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="""
Recommend one successful entrepreneur for someone with:

Occupation:
Software Engineer

Goals:
Become a CTO

Interests:
Artificial Intelligence
Leadership

Return only the person's name and a short explanation.
"""
)

print(response.text)
