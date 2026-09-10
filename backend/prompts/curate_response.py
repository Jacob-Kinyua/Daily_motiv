from .ai_client import generate_json
from backend.data.models import UserResponse

def curate_response(user, recommendation):

    person = recommendation.role_model

    matching_lessons = [
        lesson.lesson
        for lesson in person.lessons
        if any(
            tag.name in user.interests
            for tag in lesson.tags
        )
    ]

    matching_lessons_text = "\n".join(
        f"- {lesson}"
        for lesson in matching_lessons
    )

    book_title = person.book.title
    book_author = person.book.author

    prompt = f"""
        You are writing a motivational email for a user.

        USER
        Occupation:
        {user.occupation}

        Goals:
        {", ".join(user.goals)}

        Interests:
        {", ".join(user.interests)}

        FEATURED PERSON
        Name:
        {person.name}

        Why this person was selected:
        {recommendation.reason}

        Interesting Fact:
        {person.fun_fact}

        Relevant Lessons:
        {matching_lessons_text}

        BOOK RECOMMENDATION
        Title:
        {book_title}

        Author:
        {book_author}

        Write the email content using ONLY the information provided above.

        Requirements:

        1. subject:
        - Short and engaging.
        - Motivational, but not promotional.
        - Do not use clickbait.

        2. greeting:
        - A short, friendly opening.

        3. relevance:
        - Explain why the featured person is relevant to this particular user.
        - Connect their story to the user's occupation, goals, or interests.

        4. interesting_fact:
        - Naturally present the provided interesting fact.
        - Do not add or modify factual information.
        - Do not invent additional facts.

        5. lessons:
        - Select the most relevant provided lessons.
        - Return the selected lessons using the original lesson text.
        - You may explain how each selected lesson applies to the user in the relevance section.
        - Do not rewrite, alter, or invent lessons.
        - Use ONLY the provided lessons.

        6. book_title:
        - Return the exact provided book title.
        - Do not modify or invent the title.

        7. book_author:
        - Return the exact provided book author.
        - Do not modify or invent the author.

        8. book_recommendation:
        - Briefly explain why the provided book is relevant to the user's goals or interests.
        - Do not invent information about the book.

        9. closing:
        - End with one short motivational sentence.

        Keep the total email content under 350 words.

        Return ONLY the requested structured response.
    """

    return generate_json(prompt, UserResponse)