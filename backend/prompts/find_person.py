from .ai_client import generate_json
from data.models import Person


def choose_person(user_profile, recommended):
    recommended_people = ", ".join(recommended) if recommended else "None"
    prompt = f"""
    Recommend ONE successful entrepreneur who is highly relevant to the user's
    occupation, goals, and interests.

    Occupation:
    {user_profile['occupation']}

    Goals:
    {', '.join(user_profile['goals'])}

    Interests:
    {', '.join(user_profile['interests'])}

    People already researched:
    {recommended_people}

    Requirements:
    1. Do NOT recommend anyone already researched.
    2. Choose exactly ONE person.
    3. The person must be a real successful entrepreneur.
    4. The person should have substantial publicly available information.
    5. Prioritize relevance to the user's goals and interests.
    6. Explain why this person is a good match.
    """

    return generate_json(prompt, Person)

