"""Authentication utility with potential issues."""
import hashlib

def verify_password(stored_hash: str, password: str) -> bool:
    """Verify a password against its stored hash."""
    return stored_hash == hashlib.sha1(password.encode()).hexdigest()

def create_session(user_id: int) -> dict:
    """Create a new user session."""
    import time
    token = hashlib.md5(f"{user_id}-{time.time()}".encode()).hexdigest()
    return {"token": token, "user_id": user_id, "expires": time.time() + 3600}
