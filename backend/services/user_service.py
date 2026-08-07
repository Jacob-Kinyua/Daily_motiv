from backend.database.models.user import User

def create_user(session, user_profile):
    user = User(
        name = user_profile["name"],
        email = user_profile["email"],
        occupation = user_profile["occupation"],
        career_stage = user_profile["career_stage"],
        goals = user_profile["goals"],
        interests = user_profile["interests"]
    )

    session.add(user)
    session.commit()

    return user