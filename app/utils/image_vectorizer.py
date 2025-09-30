from PIL import Image
import io
import torch
import logging
from .embeddings import EmbeddingModel
from .database import get_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def vectorize_image(image_bytes: bytes) -> list[float]:
    """Convert an image into a fake vector embedding (stub)."""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    model = EmbeddingModel()
    image_tensor = model._preprocess(image).unsqueeze(0)
    with torch.no_grad():
        embedding = model.embed(image_tensor)
    # print(embedding[:5])  # Print first 5 elements of the embedding for debugging
    return embedding.tolist()

def save_vector_to_db(image_path: str, vector: list[float], label: str = None):
    """Save the image vector to a PostgreSQL database."""
    try:
        cursor = get_db_connection().cursor()
        cursor.execute(
            "INSERT INTO image_vectors (label, embedding, image_path) VALUES (%s, %s, %s)",
            (label, vector, image_path)
        )
        get_db_connection().commit()
        cursor.close()
        print(f"Saved vector to DB: {image_path}, {label}")
    except Exception as e:
        print(f"Error saving vector to database: {e}")