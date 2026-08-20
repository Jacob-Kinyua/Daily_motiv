# backend/api/main.py

from fastapi import FastAPI

from backend.api.routes.users import router as user_router
from backend.api.routes.recommendations import router as recommendation_router
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes.auth import router as auth_router



app = FastAPI(
    title="Daily Motiv API",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(recommendation_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "Daily Motiv API is running"}


