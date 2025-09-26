import numpy as np
from PIL import Image
import io
import os
import psycopg2
import torch
from torchvision import models, transforms


def vectorize_image(image_bytes: bytes) -> list[float]:
    """Convert an image into a fake vector embedding (stub)."""
    image = Image.open(io.BytesIO(image_bytes)).convert("L")  # grayscale
    arr = np.array(image.resize((32, 32))).flatten()
    vector = arr / 255.0  # normalize
    return vector.tolist()

def save_vector_to_db(filename: str, vector: list[float]):
    """Save the image vector to a PostgreSQL database."""
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO image_vectors (filename, vector) VALUES (%s, %s)",
        (filename, vector)
    )
    conn.commit()
    cursor.close()
    conn.close()