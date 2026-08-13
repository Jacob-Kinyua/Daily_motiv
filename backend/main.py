import json


from prompts.find_person import choose_person
from prompts.research_person import research_person
from prompts.score_person import score_person
from prompts.curate_response import curate_response
from data.models import RoleModelResponse

AVAILABLE_TAGS = [
    "Leadership",
    "Entrepreneurship",
    "Artificial Intelligence",
    "Software Engineering",
    "Product Development",
    "Investing & Finance",
    "Marketing & Sales",
    "Personal Development",
    "Innovation",
    "Career Growth"
]

with open("data/sample_user.json", "r") as file:
    user_profile = json.load(file)


person = choose_person(user_profile)

print(person.name)
print(person.reason)

person_details = research_person(person, AVAILABLE_TAGS)
print(person_details.fun_fact)

for lesson in person_details.lessons:
    print(lesson.lesson)
    print(lesson.tags)

print(person_details.book_recommendation.title)
print(person_details.book_recommendation.author)

person_score = score_person(person, AVAILABLE_TAGS)
print(person_score.tag_scores)


role_model_profile = RoleModelResponse(
    name=person.name,
    fun_fact=person_details.fun_fact,
    lessons=person_details.lessons,
    book_recommendation=person_details.book_recommendation,
    tag_scores=person_score.tag_scores
)




curated_response = curate_response(user_profile, person, person_details)
print(curated_response.subject)
print(curated_response.body)
