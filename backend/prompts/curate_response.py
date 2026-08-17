from .ai_client import generate_json
from backend.data.models import UserResponse

def curate_response(user, recommendation):

    person = recommendation.role_model

    matching_lessons = [
        lesson
        for lesson in person.lessons
        if any(
            tag.name in user.interests
            for tag in lesson.tags
        )
    ]

    prompt = f"""
    You are writing a motivational email.

    User

    Occupation:
    {user.occupation}

    Goals:
    {", ".join(user.goals)}

    Interests:
    {", ".join(user.interests)}

    Featured Person

    Name:
    {person.name}

    Why this person was selected:
    {recommendation.reason}

    Interesting Fact:
    {person.fun_fact}

    Relevant Lessons:
    {matching_lessons}

    Book Recommendation:
    {person.book}

    Requirements:

    - Create an engaging subject line that is short and not promotional.
    - Write a friendly and motivational email body.
    - Explain why today's featured person is relevant.
    - Mention the interesting fact naturally.
    - Ensure the fact is based on valid evidence and is verified.
    - Connect the provided lessons to the user's goals.
    - Use only the provided lessons and facts.
    - Do not invent new information.
    - Mention the recommended book naturally.
    - End with one motivational sentence.
    - Keep the email body under 350 words.
    """

    return generate_json(prompt, UserResponse)