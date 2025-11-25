#!/usr/bin/env python3
"""Verificar qual Python está sendo usado e se encontra os módulos"""

import sys
import os

print("=" * 60)
print("🔍 DIAGNÓSTICO DO PYTHON")
print("=" * 60)

print(f"\n📍 Python executável:")
print(f"   {sys.executable}")

print(f"\n📁 Diretório de trabalho:")
print(f"   {os.getcwd()}")

print(f"\n📦 PATH do Python:")
for path in sys.path:
    print(f"   {path}")

print(f"\n🔍 Testando imports...")

# Testar langchain_openai
try:
    from langchain_openai import OpenAIEmbeddings
    print("   ✅ langchain_openai - OK")
except ImportError as e:
    print(f"   ❌ langchain_openai - ERRO: {e}")
    print(f"      Tentando localizar...")
    import subprocess
    result = subprocess.run(
        ["pip", "show", "langchain-openai"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("      ✅ Pacote instalado via pip")
        for line in result.stdout.split('\n'):
            if 'Location:' in line:
                print(f"      📍 {line}")

# Testar auth
try:
    from auth import criar_token_jwt
    print("   ✅ auth - OK")
except ImportError as e:
    print(f"   ❌ auth - ERRO: {e}")

# Testar fastapi
try:
    from fastapi import FastAPI
    print("   ✅ fastapi - OK")
except ImportError as e:
    print(f"   ❌ fastapi - ERRO: {e}")

print("\n" + "=" * 60)

