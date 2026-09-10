# The Dossier — frontend

A React + Vite frontend for the inspirational-email notifier. Users "open a file"
(sign up), and the app treats their profile like a filed record — index cards,
punch holes, typewritten metadata, a stamped career-stage badge.

## Screens

- **Signup / Edit** (`src/components/SignupForm.jsx`) — one form used for both
  creating and editing a profile: name, email, occupation, career goals, career
  stage (starter / mid-level / top executive), and interest tags.
- **Welcome** (`src/components/WelcomePage.jsx`) — "Hello, {name}" with the
  profile summary and three actions: view past recommendations, edit file,
  unsubscribe.
- **Past recommendations** (`src/components/PastRecommendations.jsx`) — list of
  previously sent people/fun-facts/lessons.
- **Unsubscribe modal** (`src/components/UnsubscribeModal.jsx`) — confirmation
  before unsubscribing.

## Running it

```bash
npm install
npm run dev
```

The dev server proxies `/api/*` requests to `http://localhost:5000` (see
`vite.config.js`) — update that target if your Flask app runs elsewhere.

```bash
npm run build   # production build to dist/
```

## Backend contract this frontend expects

The frontend calls a JSON API under `/api` (`src/api.js`). Adjust field names
there to match your actual Pydantic schemas / SQLAlchemy models if they differ.

| Method | Path                              | Purpose                              |
|--------|------------------------------------|---------------------------------------|
| POST   | `/api/users`                      | Create a subscriber (signup)          |
| GET    | `/api/users/:id`                  | Fetch a subscriber                    |
| PUT    | `/api/users/:id`                  | Update a subscriber's profile         |
| POST   | `/api/users/:id/unsubscribe`      | Mark a subscriber unsubscribed        |
| GET    | `/api/users/:id/recommendations`  | List previously sent recommendations  |

**User** shape:

```json
{
  "id": "uuid-or-int",
  "name": "Ada Okafor",
  "email": "ada@example.com",
  "occupation": "Product Designer",
  "career_goals": "Move into a design leadership role within 3 years.",
  "career_stage": "mid_level",
  "interests": ["Leadership", "Product Development"],
  "subscribed": true
}
```

`career_stage` is one of `starter`, `mid_level`, `top_executive`.
`interests` is a subset of the fixed tag list in `src/constants.js`.

**Recommendation** shape:

```json
{
  "id": "uuid-or-int",
  "person_name": "Indra Nooyi",
  "person_title": "Former CEO, PepsiCo",
  "fun_fact": "She wrote personal letters to the parents of her top executives.",
  "lessons": [
    "Bring your whole self — and your team's families — into how you lead.",
    "Long tenure compounds trust; think in decades, not quarters."
  ],
  "sent_at": "2026-08-10T09:00:00Z"
}
```

## Notes / assumptions

- There's no separate login step: after signup, the returned `user.id` is
  stored in `localStorage` so returning visitors land straight on their
  Welcome page. If you want real authentication (e.g. magic-link or password),
  swap the `localStorage` bit in `src/App.jsx` for your auth flow — everything
  else (forms, views) stays the same.
- Email is treated as immutable after signup in the edit form (common for a
  notification list tied 1:1 to an inbox). Remove `disabled` on that field in
  `SignupForm.jsx` if you want it editable.
- Interest tags are hard-coded in `src/constants.js` to match the list you
  provided — update there if the taxonomy changes.
- No CSS framework/build step beyond plain CSS — all design tokens live in
  `src/index.css` so they're easy to retheme in one place.


## codes to run
uvicorn backend.api.main:app --reload
npm run dev



