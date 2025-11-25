"""
Script para testar conexão com o banco de dados
Execute: python backend/test_connection.py
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "ideias"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "senha123"),
    "port": os.getenv("DB_PORT", "5432"),
}

print("🔌 Testando conexão com o banco de dados...")
print(f"   Host: {DB_CONFIG['host']}")
print(f"   Database: {DB_CONFIG['database']}")
print(f"   User: {DB_CONFIG['user']}")
print(f"   Port: {DB_CONFIG['port']}")
print()

try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("✅ Conexão estabelecida com sucesso!")
    
    with conn.cursor() as cur:
        # Testar query simples
        cur.execute("SELECT COUNT(*) FROM ideias")
        count = cur.fetchone()[0]
        print(f"✅ Tabela 'ideias' existe e tem {count} registro(s)")
        
        # Verificar extensão pgvector
        cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector'")
        if cur.fetchone():
            print("✅ Extensão pgvector está instalada")
        else:
            print("⚠️  Extensão pgvector NÃO está instalada")
    
    conn.close()
    print("\n🎉 Tudo funcionando corretamente!")
    
except psycopg2.OperationalError as e:
    print(f"❌ Erro de conexão: {e}")
    print("\n🔧 Verifique:")
    print("   1. PostgreSQL está rodando?")
    print("   2. Banco 'ideias' existe?")
    print("   3. Usuário e senha estão corretos?")
except Exception as e:
    print(f"❌ Erro: {e}")

