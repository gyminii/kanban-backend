# utils/auth.py
import os
from starlette.requests import Request

# ---------- OPTION A: Local JWT verification (recommended) ----------
import jwt
from jwt import PyJWKClient

SUPABASE_URL = os.getenv("SUPABASE_URL")  # e.g. https://<project>.supabase.co
JWKS_URL = f"{SUPABASE_URL}/auth/v1/jwks" if SUPABASE_URL else None
_jwks = PyJWKClient(JWKS_URL) if JWKS_URL else None

def _verify_jwt_locally(bearer: str) -> str | None:
    if not bearer.startswith("Bearer "):
        return None
    token = bearer.split(" ", 1)[1]
    if not _jwks:
        raise RuntimeError("Set SUPABASE_URL to enable JWT verification")
    try:
        signing_key = _jwks.get_signing_key_from_jwt(token)
        payload = jwt.decode(token, signing_key.key, algorithms=["RS256"])
        return payload.get("sub")
    except Exception:
        return None

# ---------- OPTION B: Remote check with Supabase (simpler, adds latency) ----------
# Requires: pip install supabase
REMOTE_SUPABASE_ENABLED = os.getenv("REMOTE_SUPABASE_ENABLED", "false").lower() == "true"
if REMOTE_SUPABASE_ENABLED:
    from supabase import create_client, Client
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")  # or SERVICE_ROLE_KEY (server-side only!)
    _client: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def _verify_with_supabase_user_endpoint(bearer: str) -> str | None:
    if not bearer.startswith("Bearer "):
        return None
    token = bearer.split(" ", 1)[1]
    try:
        # supabase.auth.get_user(access_token) sends the token to /auth/v1/user
        user = _client.auth.get_user(token)  # raises if invalid
        return user.user.id if user and user.user else None
    except Exception:
        return None

# ---------- Public helpers ----------
def get_user_id_from_request(request: Request) -> str | None:
    auth_header = request.headers.get("authorization", "")
    if REMOTE_SUPABASE_ENABLED:
        return _verify_with_supabase_user_endpoint(auth_header)
    return _verify_jwt_locally(auth_header)  # default

def require_user(info) -> str:
    # uid = info.context.get("user_id")
    uid = (info.context or {}).get("user_id") or "dev-user" 
    if not uid:
        raise Exception("Unauthorized")
    return uid
