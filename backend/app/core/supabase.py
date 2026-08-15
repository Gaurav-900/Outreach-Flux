import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

supabase_url: str = os.environ.get("SUPABASE_URL", "")
supabase_service_key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

if not supabase_url or not supabase_service_key:
    raise ValueError("Missing Supabase credentials in .env")

# Using the service role key to bypass RLS, mirroring the Node.js implementation
supabase: Client = create_client(supabase_url, supabase_service_key)
