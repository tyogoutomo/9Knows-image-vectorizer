-- Create the vector extension first
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table for storing image vectors
CREATE TABLE IF NOT EXISTS image_vectors (
    id SERIAL PRIMARY KEY,
    label text NULL,
    image_path text NULL,
    embedding vector(2048) NULL,  -- Using pgvector type
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_image_vectors_image_path ON image_vectors(image_path);
CREATE INDEX IF NOT EXISTS idx_image_vectors_created_at ON image_vectors(created_at);
CREATE INDEX IF NOT EXISTS idx_image_vectors_embedding ON image_vectors USING ivfflat (embedding vector_cosine_ops);