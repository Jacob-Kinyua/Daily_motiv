import os
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_email(user_email: str, subject: str, body: str):

    params = {
        "from": "Daily Inspiron <onboarding@resend.dev>",
        "to": [user_email],
        "subject": subject,
        "text": body,
    }

    email = resend.Emails.send(params)

    return True