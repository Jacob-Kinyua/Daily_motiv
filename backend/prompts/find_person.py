from google import genai
from dotenv import load_dotenv
import os, json

load_dotenv()

with open("../data/sample_user.json", "r") as file:
    user_profile = json.load(file)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=f"""
Recommend one successful entrepreneur for someone with:

Occupation:
{user_profile['occupation']}

Goals:
{', '.join(user_profile['goals'])}

Interests:
{', '.join(user_profile['interests'])}

Return only the person's name and a short explanation.
"""
)

print(response.text)
