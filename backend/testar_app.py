#!/usr/bin/env python3
"""Testar se o app.py pode ser importado sem erros"""

print("🧪 Testando importação do app.py...")
print("")

try:
    import app
    print("✅ app.py importado com sucesso!")
    print(f"   App criado: {app.app}")
    print("   ✅ Backend pronto para iniciar!")
except Exception as e:
    print(f"❌ Erro ao importar app.py:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("")
print("🚀 Você pode iniciar o backend agora:")
print("   python -m uvicorn app:app --host 0.0.0.0 --port 8002")

