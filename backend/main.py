import json

from prompts.find_person import choose_person
# from prompts.research_person import research_person

with open("data/sample_user.json", "r") as file:
    user_profile = json.load(file)


person = choose_person(user_profile)
print(person["name"])
print(person["reason"])
