import os
import bcrypt
from supabase import create_client

SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://sdfviglipthprhkzetkl.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNkZnZpZ2xpcHRocHJoa3pldGtsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MzUwNTc0NywiZXhwIjoyMDg5MDgxNzQ3fQ.BspWRcoyCKABIzrv-ONOqD3btIppPm5ESDwnyekJyPM")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def signup(full_name: str, email: str, password: str, year: str, cgpa: str, branch: str) -> dict:
    """Register new user. Returns {"success": True, "user": {...}} or {"success": False, "error": "..."}"""
    try:
        # Check if email already exists
        existing = supabase.table("users").select("id").eq("email", email).execute()
        if existing.data:
            return {"success": False, "error": "Email already registered!"}

        # Hash password
        password_hash = hash_password(password)

        # Insert user
        result = supabase.table("users").insert({
            "full_name":     full_name,
            "email":         email,
            "password_hash": password_hash,
            "year":          year,
            "cgpa":          cgpa,
            "branch":        branch,
        }).execute()

        if result.data:
            return {"success": True, "user": result.data[0]}
        return {"success": False, "error": "Signup failed!"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def login(email: str, password: str) -> dict:
    """Login user. Returns {"success": True, "user": {...}} or {"success": False, "error": "..."}"""
    try:
        result = supabase.table("users").select("*").eq("email", email).execute()

        if not result.data:
            return {"success": False, "error": "Email not found!"}

        user = result.data[0]

        if not verify_password(password, user["password_hash"]):
            return {"success": False, "error": "Wrong password!"}

        return {"success": True, "user": user}

    except Exception as e:
        return {"success": False, "error": str(e)}


def get_all_users() -> list:
    """Admin — get all registered users."""
    try:
        result = supabase.table("users").select("full_name, email, year, cgpa, branch, created_at").execute()
        return result.data or []
    except:
        return []