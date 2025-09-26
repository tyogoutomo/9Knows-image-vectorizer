from fastapi import FastAPI
from app.routers import vectorizer

app = FastAPI(title="Image Vectorizer API", version="1.0.0")

# Routers
app.include_router(vectorizer.router)

@app.get("/")
def root():
    return {"message": "Image Vectorizer API is running"}
