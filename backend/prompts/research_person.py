from .ai_client import generate_json
from .models import ResearchResponse

def research_person(target_person, tags):

    prompt = f"""
You are researching the following successful person:

{target_person.name}

Available tags:
{", ".join(tags)}

Requirements:

1. Generate one interesting fact.
2. Generate between 5 and 10 lessons from their life.
3. Assign one or more tags to each lesson.
4. Only use tags from the available tag list.
5. Recommend one biography or book written by or about this person.
"""

    return generate_json(prompt, ResearchResponse)