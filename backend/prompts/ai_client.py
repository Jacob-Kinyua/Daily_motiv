# from google import genai
# from google.genai import types
# from dotenv import load_dotenv
# import os, json

# load_dotenv()


# client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# def generate_json(prompt, schema):
#     response = client.models.generate_content(
#         model="gemini-3.5-flash",
#         contents=prompt,
#         config=types.GenerateContentConfig(
#             response_mime_type="application/json",
#             response_schema=schema,
#         )
#     )

#     return response.parsed

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def generate_json(prompt, schema):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                )
            )

            return response.parsed

        except Exception as e:
            error_message = str(e)

            # Retry temporary API errors
            if "503" in error_message or "429" in error_message:

                if attempt == max_retries - 1:
                    raise

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                # Don't retry other errors
                raise