# backend/api/main.py

from fastapi import FastAPI

app = FastAPI(
    title="Daily Motiv API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "Daily Motiv API is running"}


