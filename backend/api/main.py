# backend/api/main.py

from fastapi import FastAPI

from backend.api.routes.users import router as user_router
from backend.api.routes.recommendations import router as recommendation_router

app = FastAPI(
    title="Daily Motiv API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(recommendation_router)

@app.get("/")
def root():
    return {"message": "Daily Motiv API is running"}


