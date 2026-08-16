from fastapi import Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.supabase import supabase

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Dependency to validate Supabase JWT and get the authenticated user.
    """
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        if not user_response.user:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        return user_response.user
    except Exception as e:
        print(f"Auth error: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid authentication token")
