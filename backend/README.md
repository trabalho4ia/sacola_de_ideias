# 🐍 Backend Python - Sacola de Ideias

Backend FastAPI para conectar com PostgreSQL usando pgvector.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- PostgreSQL com pgvector instalado
- Banco de dados `ideias` criado

## 🚀 Instalação

### 1. Instalar dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

O arquivo `.env` já está configurado com:
- DB_NAME=ideias
- DB_PASSWORD=senha123

Se precisar alterar, edite o arquivo `.env`:

```env
DB_HOST=localhost
DB_NAME=ideias
DB_USER=postgres
DB_PASSWORD=senha123
DB_PORT=5432
```

### 3. Iniciar o servidor

```bash
python app.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn app:app --reload --port 8000
```

O servidor estará rodando em: `http://localhost:8000`

## 📚 Documentação da API

Com o servidor rodando, acesse:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🔌 Endpoints Disponíveis

- `GET /api/ideias` - Listar todas as ideias
- `GET /api/ideias/{id}` - Buscar ideia por ID
- `POST /api/ideias` - Criar nova ideia
- `POST /api/ideias/com-embedding` - Criar ideia com embedding
- `PUT /api/ideias/{id}` - Atualizar ideia
- `PUT /api/ideias/{id}/embedding` - Atualizar embedding
- `DELETE /api/ideias/{id}` - Deletar ideia
- `POST /api/ideias/buscar` - Buscar por similaridade

## 🧪 Testar a API

```bash
# Listar ideias
curl http://localhost:8000/api/ideias

# Criar ideia
curl -X POST http://localhost:8000/api/ideias \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Minha Ideia", "tag": "teste", "ideia": "Conteúdo da ideia"}'

# Buscar por ID
curl http://localhost:8000/api/ideias/1
```

## 🔧 Troubleshooting

### Erro de conexão com banco
- Verifique se o PostgreSQL está rodando: `sudo service postgresql status`
- Verifique as credenciais no arquivo `.env`
- Teste a conexão: `psql -U postgres -d ideias`

### Erro ao instalar psycopg2
```bash
# Instalar dependências do sistema
sudo apt-get install python3-dev libpq-dev

# Depois instalar novamente
pip install psycopg2-binary
```

