from .ai_client import generate_json
from data.models import UserResponse

def curate_response(user_profile, person, research_response):
    matching_lessons = [
        lesson
        for lesson in research_response.lessons
        if any(
            tag in user_profile["interests"]
            for tag in lesson.tags
        )
    ]
    prompt = f"""
    You are writing a motivational email.

    User

    Occupation:
    {user_profile["occupation"]}

    Goals:
    {", ".join(user_profile["goals"])}

    Interests:
    {", ".join(user_profile["interests"])}

    Featured Person

    Name:
    {person.name}

    Why this person was selected:
    {person.reason}

    Interesting Fact:
    {research_response.fun_fact}

    Relevant Lessons:
    {matching_lessons}

    Book Recommendation:
    {research_response.book_recommendation}


    Requirements: 

    - Create an engaging subject line.
    - Write a friendly and motivational email body.
    - Explain why today's featured person is relevant.
    - Mention the interesting fact naturally.
    - Connect the provided lessons to the user's goals.
    - Use only the provided lessons and facts.
    - Do not invent new information.
    - Mention the recommended book naturally.
    - End with one motivational sentence.
    - Keep the email body under 350 words.
    """

    return generate_json(prompt, UserResponse)