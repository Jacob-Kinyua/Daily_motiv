from google import genai
from dotenv import load_dotenv
import os, json

load_dotenv()


client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def choose_person(user_profile):
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

    Return ONLY valid JSON.

    The JSON must have exactly this format:

    {{
        "name": "",
        "reason": ""
    }}

    Do not use markdown.
    Do not wrap the JSON in triple backticks.
    Do not include any extra text.
    """
    )

    return json.loads(response.text)
