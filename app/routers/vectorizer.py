from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.image_vectorizer import vectorize_image

router = APIRouter(prefix="/api", tags=["vectorizer"])

@router.post("/vectorize")
async def vectorize(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")
    
    contents = await file.read()
    vector = vectorize_image(contents)
    return {"filename": file.filename, "vector_length": len(vector), "vector": vector[:20]}  
    # returning only first 20 values to avoid massive   JSON
