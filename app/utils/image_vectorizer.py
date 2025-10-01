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
    
    # Normalize the embedding to unit length
    normalized = embedding / torch.norm(embedding, p=2)
    return normalized.tolist()

def save_vector_to_db(image_path: str, vector: list[float], platform: str = None, page: str = None, repo_source: str = None, feature_related: str = None):
    """Save the image vector to a PostgreSQL database."""
    try:
        cursor = get_db_connection().cursor()
        cursor.execute(
            "INSERT INTO image_vectors (platform, page_name, repo_source, feature_related, embedding, image_path) VALUES (%s, %s, %s, %s, %s, %s)",
            (platform, page, repo_source, feature_related, vector, image_path)
        )
        get_db_connection().commit()
        cursor.close()
        print(f"Saved vector to DB: {image_path}, {platform}, {page}, {repo_source}, {feature_related}")
    except Exception as e:
        print(f"Error saving vector to database: {e}")
        return str(e)