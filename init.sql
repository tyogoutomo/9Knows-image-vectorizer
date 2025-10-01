-- Create the vector extension first
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table for storing image vectors
CREATE TABLE IF NOT EXISTS image_vectors (
    id SERIAL PRIMARY KEY,
    page_id text NULL,
    repo_source text NULL,
    feature_related text NULL,
    image_path text NULL,
    embedding vector(2048) NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_image_vectors_image_path ON image_vectors(image_path);
CREATE INDEX IF NOT EXISTS idx_image_vectors_created_at ON image_vectors(created_at);

-- Skip the vector index for now - will do sequential scan
-- CREATE INDEX IF NOT EXISTS idx_image_vectors_embedding ON image_vectors USING ivfflat (embedding vector_cosine_ops);