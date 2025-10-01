-- Create the vector extension first
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table for storing image vectors
CREATE TABLE IF NOT EXISTS image_vectors (
    id SERIAL PRIMARY KEY,
    platform text NULL, -- Platform: rumah123 web/99co ID web / rumah123 proapp / etc
    page_name text NULL, -- page: Homepage / SRP / LDP / PDP / etc
    repo_source text NULL, -- repo: urbanindo/core-web
    feature_related text NULL, -- feature: banner / header / properti rekomendasi / etc
    image_path text NULL,
    embedding vector(2048) NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_image_vectors_image_path ON image_vectors(image_path);
CREATE INDEX IF NOT EXISTS idx_image_vectors_created_at ON image_vectors(created_at);
