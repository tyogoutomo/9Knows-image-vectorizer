from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.utils.image_vectorizer import save_vector_to_db, vectorize_image
from app.utils.similarity_vector_search import find_most_similar_images

router = APIRouter(prefix="/api", tags=["vectorizer"])

@router.post("/vectorize")
async def vectorize(
    file: UploadFile = File(...),
    label: str = Form(None)
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Must be an image.")

    contents: bytes = await file.read()
    vector = vectorize_image(contents)
    save_vector_to_db(file.filename, vector, label)

    return {
        "status": "success",
        "filename": file.filename,
        "label": label,
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
    
    print("Most similar images:")
    labels = []
    for result in similar_images:
        print(f"Image: {result['image_path']}, Label: {result['label']}, Distance: {result['distance']}")
        labels.append(result['label'])

    return {
        "status": "success",
        "filename": file.filename,
        "similar_images": similar_images,
        "labels": labels,
    }
