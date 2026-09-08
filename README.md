# Daily Motiv

Daily Motiv is a personalized motivation and career-growth platform that connects users with successful role models based on their career goals, occupation, and interests.

Users create a profile describing where they are in their career and what they want to achieve. The application uses AI to select and research a relevant role model, identify lessons from their career, recommend a book, and generate a personalized motivational email.

## Features

* Create a personalized user profile
* Select career stage and interests
* AI-powered role model recommendations
* Research successful role models and extract:

  * Interesting facts
  * Career lessons
  * Relevant tags
  * Book recommendations
* Rank existing role models based on user interests
* Avoid recommending the same role model to a user twice
* Generate personalized motivational emails
* View previous recommendations
* Unsubscribe by deleting the user's profile

## How It Works

The recommendation process follows several steps:

```text
                         User
                           │
             ┌─────────────┴─────────────┐
             │                           │
       New User                      Existing User
             │                           │
             ▼                           ▼
       Create Profile                Login Page
             │                           │
             ├── Name                    │
             ├── Email                   │
             ├── Occupation              │
             ├── Career Goals             │
             ├── Career Stage             │
             └── Interests                │
             │                           │
             ▼                           │
       Login / Verification ◄────────────┘
             │
             ▼
      Enter Verification Code
             │
             ▼
        Email Verified
             │
             ▼
          Logged In
             │
             ▼
   ┌─────────────────────────┐
   │  Recommendation Engine  │
   └─────────────────────────┘
             │
             ▼
    Check Existing Role Models
             │
       ┌─────┴──────┐
       │            │
       ▼            ▼
    Suitable      No Suitable
    Role Model    Role Model
       │            │
       ▼            ▼
  Rank by Tag     AI Generates
     Scores        New Role Model
       │            │
       │            ▼
       │       Research Person
       │            │
       │            ▼
       │       Score Relevant
       │           Tags
       │            │
       │            ▼
       │       Save to Database
       │            │
       └──────┬─────┘
              │
              ▼
    Create Recommendation
              │
              ▼
 Generate Personalized Email
              │
              ▼
             User
```


## AI Pipeline

The AI portion of the application is divided into several prompts:

### 1. Find a Person

The application provides the user's profile and previously stored role models to the AI.

The AI selects a successful person who is relevant to the user's goals and interests and has not already been stored.

### 2. Research the Person

The selected person is researched to generate:

* An interesting fact
* Career lessons
* Relevant interest tags
* A recommended book

### 3. Score the Person

The role model is scored against the application's available tags.

These scores are stored alongside the role model and are later used to rank potential recommendations.

### 4. Curate the Response

The user's profile, role model information, and relevant lessons are passed to the final prompt.

The AI generates:

* A personalized email subject
* A motivational email body

## Recommendation System

Daily Motiv stores role models in the database rather than generating a completely new person for every user.

When generating a recommendation:

1. Retrieve role models the user has not previously received.
2. Find role models with tags matching the user's interests.
3. Sum the relevant tag scores.
4. Rank the candidates.
5. Select the highest-ranked role model.
6. If no suitable role model exists, generate a new one using AI.
7. Store the recommendation so the same person is not recommended again.

## Features

The dashboard allows for the following features
```text
                    Dashboard
                        │
        ┌───────────────┼────────────────┐
        │               │                │
        ▼               ▼                ▼
   Profile          Recommendations   Account
        │               │                │
   ┌────┴────┐      ┌───┴────┐      ┌───┴────┐
   │         │      │        │      │        │
   ▼         ▼      ▼        ▼      ▼        ▼
  View      Edit   Past    Generate Logout  Unsubscribe
 Profile   Profile Recs.   New Rec.
                           │
                           ▼
                     Email + Dashboard
```

### Passwordless email authentication 

Users verify their email with a one-time code when signing up or logging in.

### Personalized dashboard 

Users can view and edit their profile information.

### Recommendation history 

Users can view their previous role-model recommendations. 

### On-demand recommendations 

Users without recommendations can generate one directly from the dashboard.

### Email + dashboard delivery 

Newly generated recommendations are sent to the user's email and displayed on the past recommendations page.

### Account management 

Users can log out or unsubscribe and remove their account.

### AI-powered recommendations 

The system selects and ranks role models based on the user's interests and career goals.

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* PostgreSQL

### Frontend

* React
* JavaScript
* Vite

### AI

* Google Gemini / Google GenAI

### Email

* SMTP

### Database

* PostgreSQL
* Supabase for hosted database development/deployment

## Project Structure

```text
Daily_motiv/
│
├── backend/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── users.py
│   │       └── recommendations.py
│   │
│   ├── database/
│   │   ├── models/
│   │   └── session.py
│   │
│   ├── prompts/
│   │   ├── ai_client.py
│   │   ├── find_person.py
│   │   ├── research_person.py
│   │   ├── score_person.py
│   │   └── curate_response.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── role_model_service.py
│   │   ├── recommendation_service.py
│   │   └── generate_email.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   └── recommendation.py
│   │
│   └── constants/
│       └── tags.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
|   |   |   ├── loginPge.jsx
|   |   |   ├── PastRecommendations.jsc
|   |   |   ├── SignupForm.jsx
|   |   |   ├── UnsubscribeModal.jsx
|   |   |   ├── WelcomePage.jsx
│   │   ├── api.js
│   │   ├── constants.js
│   │   ├── index.css
│   │   ├── main.jsx
│   │   └── App.jsx
│   │
│   └── package.json
│
├── alembic/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## API Endpoints

### Users

| Method | Endpoint           | Description               |
| ------ | ------------------ | ------------------------- |
| POST   | `/users/`          | Create a user             |
| DELETE | `/users/{user_id}` | Delete/unsubscribe a user |

### Recommendations

| Method | Endpoint                     | Description                                |
| ------ | ---------------------------- | ------------------------------------------ |
| POST   | `/recommendations/{user_id}` | Generate and send a recommendation         |
| GET    | `/recommendations/{user_id}` | Retrieve the user's recommendation history |

## Running Locally

### 1. Clone the repository

```bash
git clone <repository-url>
cd Daily_motiv
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url
GEMINI_API_KEY=your_gemini_api_key

MY_EMAIL=your_email
MY_PASSWORD=your_email_password
```

Do not commit `.env` to GitHub.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the backend

From the project root:

```bash
uvicorn backend.api.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API documentation:

```text
http://localhost:8000/docs
```

### 7. Start the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will then be available at the URL provided by Vite.

## Environment Variables

| Variable         | Description                                    |
| ---------------- | ---------------------------------------------- |
| `DATABASE_URL`   | PostgreSQL database connection string          |
| `GEMINI_API_KEY` | API key used for AI generation                 |
| `MY_EMAIL`       | Email account used for sending recommendations |
| `MY_PASSWORD`    | Email account credentials/app password         |

## Current Limitations

This project is currently an MVP.

* Email delivery currently uses SMTP and may be classified as spam by email providers.
* Authentication is not currently implemented.
* Users are identified by their database ID.
* Unsubscribing currently removes the user's stored information.
* Recommendation emails are currently triggered through the API while automated scheduling is being developed.
* AI-generated information depends on the quality and accuracy of the underlying model responses.

## Future Improvements

* Add user authentication
* Add automated daily/weekly email scheduling
* Improve email deliverability using a transactional email provider
* Add unsubscribe links directly to emails
* Improve role-model ranking
* Add more personalization signals
* Add recommendation diversity to prevent overly similar recommendations
* Add analytics for email delivery and engagement
* Deploy the frontend and backend

## Project Goal

The goal of Daily Motiv is to make career inspiration more personalized and actionable.

Instead of receiving generic motivational content, users receive stories from successful people whose careers, experiences, and lessons are relevant to where they want to go.
