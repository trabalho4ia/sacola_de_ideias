-- ============================================
-- Script de Criação do Banco de Dados
-- Sacola de Ideias - PostgreSQL com pgvector
-- ============================================

-- 1. Criar extensão pgvector (se ainda não existir)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Criar tabela de ideias
CREATE TABLE IF NOT EXISTS ideias (
    id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tag VARCHAR(100),
    ideia TEXT NOT NULL,
    data TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    embedding vector(1536)  -- OpenAI text-embedding-3-small usa 1536 dimensões
);

-- 3. Criar índices para melhorar performance
-- Índice para busca por título e tag (busca textual)
CREATE INDEX IF NOT EXISTS idx_ideias_titulo ON ideias USING gin(to_tsvector('portuguese', titulo));
CREATE INDEX IF NOT EXISTS idx_ideias_tag ON ideias(tag);
CREATE INDEX IF NOT EXISTS idx_ideias_data ON ideias(data DESC);

-- Índice HNSW para busca por similaridade vetorial (pgvector)
-- Este é o índice mais importante para busca por IA
CREATE INDEX IF NOT EXISTS idx_ideias_embedding 
ON ideias 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 4. Criar função para atualizar updated_at automaticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 5. Criar trigger para atualizar updated_at
DROP TRIGGER IF EXISTS update_ideias_updated_at ON ideias;
CREATE TRIGGER update_ideias_updated_at
    BEFORE UPDATE ON ideias
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- 6. Função para buscar ideias por similaridade (usando cosine distance)
CREATE OR REPLACE FUNCTION buscar_ideias_por_similaridade(
    query_embedding vector(1536),
    similarity_threshold FLOAT DEFAULT 0.5,
    max_results INT DEFAULT 10
)
RETURNS TABLE (
    id BIGINT,
    titulo VARCHAR(255),
    tag VARCHAR(100),
    ideia TEXT,
    data TIMESTAMP WITH TIME ZONE,
    similarity FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id,
        i.titulo,
        i.tag,
        i.ideia,
        i.data,
        -- Cosine similarity: 1 - cosine_distance = similarity
        -- Quanto maior o valor, mais similar
        1 - (i.embedding <=> query_embedding) AS similarity
    FROM ideias i
    WHERE i.embedding IS NOT NULL
    AND (1 - (i.embedding <=> query_embedding)) >= similarity_threshold
    ORDER BY i.embedding <=> query_embedding  -- Ordenar por menor distância (mais similar primeiro)
    LIMIT max_results;
END;
$$ LANGUAGE plpgsql;

-- 7. Comentários nas colunas para documentação
COMMENT ON TABLE ideias IS 'Tabela principal para armazenar ideias e anotações';
COMMENT ON COLUMN ideias.embedding IS 'Embedding vetorial gerado pela OpenAI para busca por similaridade';
COMMENT ON COLUMN ideias.titulo IS 'Título da ideia ou anotação';
COMMENT ON COLUMN ideias.tag IS 'Tag opcional para categorização';
COMMENT ON COLUMN ideias.ideia IS 'Conteúdo completo da ideia ou anotação';

