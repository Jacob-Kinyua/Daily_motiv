import smtplib
import os
from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")


def send_email(user_email: str, subject: str, body: str):

    message = EmailMessage()

    message["From"] = MY_EMAIL
    message["To"] = user_email
    message["Subject"] = subject

    message.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL,password=MY_PASSWORD)

        connection.send_message(message)

    return True

