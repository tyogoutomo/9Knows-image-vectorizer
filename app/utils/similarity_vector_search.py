import numpy as np
import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)

def find_most_similar_images(query_embedding, top_n=3):
    """Find the most similar images using pgvector similarity search."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # DEBUG PRINT
        # Check if we have any data first
        cursor.execute("SELECT COUNT(*) FROM image_vectors WHERE embedding IS NOT NULL")
        count = cursor.fetchone()[0]
        print(f"Total records with embeddings: {count}")
        
        if count == 0:
            return []
        
        # Convert query_embedding to proper format for pgvector
        if isinstance(query_embedding, list):
            vector_str = '[' + ','.join(map(str, query_embedding)) + ']'
        else:
            vector_str = '[' + ','.join(map(str, query_embedding.tolist())) + ']'
        
        # Use pgvector cosine similarity operator
        query = """
            SELECT image_path, page_id, repo_source, feature_related,
                1 - (embedding <=> %s) AS cosine_similarity
            FROM image_vectors
            WHERE embedding IS NOT NULL
            ORDER BY cosine_similarity DESC
            LIMIT %s;
        """
        
        cursor.execute(query, (vector_str, top_n))
        similar_images = cursor.fetchall()
        
        # DEBUG PRINT
        print("Similar images found:", similar_images)
        
        # Format the results
        results = []
        for image_path, page_id, repo_source, feature_related, cosine_similarity in similar_images:
            results.append({
                "image_path": image_path,
                "page_id": page_id,
                "repo_source": repo_source,
                "feature_related": feature_related,
                "cosine_similarity": float(cosine_similarity) if cosine_similarity is not None else 1.0
            })
        
        return results
        
    except Exception as e:
        logger.error(f"Error in similarity search: {e}")
        if conn:
            conn.rollback()  # Rollback the failed transaction
        raise
        
    finally:
        if cursor:
            cursor.close()