from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.image_vectorizer import save_vector_to_db, vectorize_image
from app.utils.similarity_vector_search import find_most_similar_images
from app.utils.database import clear_table

router = APIRouter(prefix="/api", tags=["vectorizer"])

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    platform: str = Form(None),
    page: str = Form(None),
    repo_source: str = Form(None),
    feature_related: str = Form(None)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")

    contents: bytes = await file.read()
    vector = vectorize_image(contents)
    err = save_vector_to_db(file.filename, vector, platform, page, repo_source, feature_related)

    if err:
        return {
            "status": "failed",
            "filename": file.filename,
            "error": err,
        }

    return {
        "status": "success",
        "filename": file.filename,
        "vector_length": len(vector),
    }

@router.post("/similarity")
async def similarity(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")
    
    contents: bytes = await file.read()
    vector = vectorize_image(contents)
    
    # Perform similarity search query
    similar_images = find_most_similar_images(vector)

    return {
        "status": "success",
        "filename": file.filename,
        "similar_images": similar_images,
    }

@router.post("/clear")
async def clear():
    clear_table()
    return {"status": "success", "message": "All vectors cleared from the database."}
