from supabase import create_client

SUPABASE_URL = "https://cldvwgtcfuuhziqelljf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNsZHZ3Z3RjZnV1aHppcWVsbGpmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NDA4OTAxOCwiZXhwIjoyMDc5NjY1MDE4fQ.N0SeK0cEL83uIuY_-NsWqTWGJ4olqMadr0rNfrfLEE8"  # eu te ensino onde pegar

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
