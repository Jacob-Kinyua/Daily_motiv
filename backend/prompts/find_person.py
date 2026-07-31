from .ai_client import generate_json
from data.models import Person


def choose_person(user_profile):
    prompt = f"""
    Recommend one successful entrepreneur for someone with:

    Occupation:
    {user_profile['occupation']}

    Goals:
    {', '.join(user_profile['goals'])}

    Interests:
    {', '.join(user_profile['interests'])}
    """

    return generate_json(prompt, Person)

