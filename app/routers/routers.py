from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.image_vectorizer import save_vector_to_db, vectorize_image
from app.utils.similarity_vector_search import find_most_similar_images
from app.utils.database import clear_table

router = APIRouter(prefix="/api", tags=["vectorizer"])

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    page_id: str = Form(None),
    repo_source: str = Form(None),
    feature_related: str = Form(None)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")

    contents: bytes = await file.read()
    vector = vectorize_image(contents)
    save_vector_to_db(file.filename, vector, page_id, repo_source, feature_related)

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
    
    # DEBUG PRINT
    print("Most similar images:")
    page_ids = []
    for result in similar_images:
        print(f"Image: {result['image_path']}, Page ID: {result['page_id']}, Repo Source: {result['repo_source']}, Feature Related: {result['feature_related']}, Cosine Similarity: {result['cosine_similarity']}")
        page_ids.append(result['page_id'])

    return {
        "status": "success",
        "filename": file.filename,
        "similar_images": similar_images,
        "page_ids": page_ids
    }

@router.post("/clear")
async def clear():
    clear_table()
    return {"status": "success", "message": "All vectors cleared from the database."}
