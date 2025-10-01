import numpy as np
import logging
from .database import get_db_connection

logger = logging.getLogger(__name__)
SIMILARITY_THRESHOLD = 0.2 ## TODO: NEED TO BE MODIFY BASED ON DATA EXPLORATION

def find_most_similar_images(query_embedding, top_n=3):
    """Find the most similar images using pgvector similarity search."""
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check record count
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
        
        query = """
            SELECT image_path, platform, page_name, repo_source, feature_related,
                1 - (embedding <=> %s) AS cosine_similarity
            FROM image_vectors
            WHERE embedding IS NOT NULL
            ORDER BY cosine_similarity DESC
            LIMIT %s;
        """

        cursor.execute(query, (vector_str, top_n))
        similar_images = cursor.fetchall()
        # Format the results
        results = []
        for image_path, platform, page_name, repo_source, feature_related, similarity in similar_images:
            print("sim:", similarity, "-", feature_related)
            if similarity > SIMILARITY_THRESHOLD: # Threshold for similarity
                results.append({
                    "image_path": image_path,
                    "platform": platform,
                    "page": page_name,
                    "repo_source": repo_source,
                    "feature_related": feature_related,
                    "cosine_similarity": float(similarity) if similarity is not None else 0.0,
                })
        
        return results
        
    except Exception as e:
        logger.error(f"Error in similarity search: {e}")
        if conn:
            conn.rollback()  # Rollback failed transaction
        raise
        
    finally:
        if cursor:
            cursor.close()