import json


from prompts.find_person import choose_person
from prompts.research_person import research_person
from prompts.score_person import score_person
from prompts.curate_response import curate_response
# from data.models import RoleModelResponse
# from services.role_model_service import *
# from services.user_service import *
# from services.role_model_service import *
from services.generate_email import *

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


# existing_people = get_role_model_names()
existing_people = []

person = choose_person(user_profile, existing_people)
person_details = research_person(person, AVAILABLE_TAGS)
person_score = score_person(person, AVAILABLE_TAGS)


# role_model_profile = RoleModelResponse(
#     name=person.name,
#     fun_fact=person_details.fun_fact,
#     lessons=person_details.lessons,
#     book_recommendation=person_details.book_recommendation,
#     tag_scores=person_score.tag_scores
# )




curated_response = curate_response(user_profile, person, person_details)

print("Person:", person.name)
print("Reason:", person.reason)

print("\nEmail subject:")
print(curated_response.subject)

print("\nEmail body:")
print(curated_response.body)

sent_email = send_email("muskins18@gmail.com", curated_response.subject, curated_response.body)

if sent_email:
    print("sent email")
else:
    print("an error occurred")