import os

SUPABASE_URL=os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY=os.getenv("SUPABASE_SERVICE_KEY")
DATABASE_URL=os.getenv("DATABASE_URL")

def status():
    return {
        "provider":"supabase",
        "url": bool(SUPABASE_URL),
        "service_key": bool(SUPABASE_SERVICE_KEY),
        "database": bool(DATABASE_URL)
    }
