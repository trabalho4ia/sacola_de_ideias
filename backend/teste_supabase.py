from supabase import create_client

# URL do seu projeto no Supabase
SUPABASE_URL = "https://cldvwgtcfuuhziqelljf.supabase.co"

# Pegue em: Settings → API → service_role (NÃO USE ANON)
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsZHZ3Z3RjZnV1aHppcWVsbGpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDA4OTAxOCwiZXhwIjoyMDc5NjY1MDE4fQ.N0SeK0cEL83uIuY_-NsWqTWGJ4olqMadr0rNfrfLEE8"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def testar_conexao():
    try:
        print("🔌 Testando conexão com Supabase...")

        # Tenta buscar 1 registro da tabela ideias
        res = supabase.table("ideias").select("*").limit(1).execute()

        print("✅ Conexão ok!")
        print("Retorno:", res.data)

    except Exception as e:
        print("❌ Erro:")
        print(e)


if __name__ == "__main__":
    testar_conexao()
