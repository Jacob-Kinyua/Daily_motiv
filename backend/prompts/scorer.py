from .ai_client import generate_json
from .models import ScoreResponse


def score_person(target_person, tags):

    prompt = f"""
    You are evaluating how relevant {target_person.name} is to each of the following topics.

    Topics:
    {", ".join(tags)}

    For EACH topic:

    - Assign a relevance score from 0 to 10.
    - 0 means the person's career has almost no connection.
    - 10 means the topic is central to their career.
    - Provide one concise sentence explaining the score.

    Evaluate every topic exactly once.
    """

    return generate_json(prompt, ScoreResponse)
