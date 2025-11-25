#!/usr/bin/env python3
"""Testar se os imports estão funcionando"""

try:
    from langchain_openai import OpenAIEmbeddings
    print("✅ langchain_openai importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar langchain_openai: {e}")

try:
    import psycopg2
    print("✅ psycopg2 importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar psycopg2: {e}")

try:
    from auth import criar_token_jwt
    print("✅ auth importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar auth: {e}")

try:
    from fastapi import FastAPI
    print("✅ fastapi importado com sucesso!")
except ImportError as e:
    print(f"❌ Erro ao importar fastapi: {e}")

print("\n✅ Todos os módulos testados!")

