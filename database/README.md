# 🗄️ Banco de Dados - Sacola de Ideias

Este diretório contém os scripts SQL para configurar o banco de dados PostgreSQL com pgvector.

## 📋 Pré-requisitos

1. **PostgreSQL** 12 ou superior
2. **Extensão pgvector** instalada

### Instalar pgvector

#### Ubuntu/Debian:
```bash
sudo apt install postgresql-15-pgvector
```

#### Ou compilar do código:
```bash
git clone --branch v0.5.1 https://github.com/pgvector/pgvector.git
cd pgvector
make
sudo make install
```

## 🚀 Configuração

### 1. Criar banco de dados

```sql
CREATE DATABASE sacola_ideias;
\c sacola_ideias
```

### 2. Executar o script de schema

```bash
psql -U seu_usuario -d sacola_ideias -f database/schema.sql
```

Ou no psql:
```sql
\i database/schema.sql
```

### 3. Verificar instalação

```sql
-- Verificar extensão pgvector
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Verificar tabela criada
\d ideias

-- Verificar índices
\di ideias
```

## 📊 Estrutura da Tabela

```sql
CREATE TABLE ideias (
    id BIGSERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tag VARCHAR(100),
    ideia TEXT NOT NULL,
    data TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    embedding vector(1536)  -- Para busca por similaridade
);
```

## 🔍 Busca por Similaridade

O banco inclui uma função para buscar ideias por similaridade:

```sql
-- Exemplo de uso da função
SELECT * FROM buscar_ideias_por_similaridade(
    query_embedding := '[seu_embedding_aqui]'::vector(1536),
    similarity_threshold := 0.7,  -- Mínimo 70% de similaridade
    max_results := 10
);
```

## 📝 Exemplos de Queries

### Inserir uma ideia (sem embedding)
```sql
INSERT INTO ideias (titulo, tag, ideia)
VALUES ('Minha Ideia', 'trabalho', 'Conteúdo da ideia aqui');
```

### Atualizar embedding de uma ideia
```sql
UPDATE ideias 
SET embedding = '[array_do_embedding]'::vector(1536)
WHERE id = 1;
```

### Buscar ideias por texto (busca simples)
```sql
SELECT * FROM ideias 
WHERE titulo ILIKE '%palavra%' 
   OR ideia ILIKE '%palavra%'
ORDER BY data DESC;
```

### Buscar por similaridade vetorial
```sql
-- Usando operador <=> (cosine distance)
SELECT 
    id,
    titulo,
    tag,
    ideia,
    1 - (embedding <=> '[query_embedding]'::vector(1536)) AS similarity
FROM ideias
WHERE embedding IS NOT NULL
ORDER BY embedding <=> '[query_embedding]'::vector(1536)
LIMIT 10;
```

## 🔧 Manutenção

### Backup
```bash
pg_dump -U usuario -d sacola_ideias > backup.sql
```

### Restaurar
```bash
psql -U usuario -d sacola_ideias < backup.sql
```

### Limpar tabela (cuidado!)
```sql
TRUNCATE TABLE ideias;
```

## 📚 Referências

- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

