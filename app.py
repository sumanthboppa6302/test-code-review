"""Simple web application for user management."""
import hashlib
import sqlite3
from typing import Optional


class Database:
    """SQLite database wrapper for user operations."""
    
    def __init__(self, db_path: str = "users.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
    
    def create_user(self, username: str, email: str, password: str) -> int:
        """Create a new user and return their ID."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor = self.conn.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user(self, user_id: int) -> Optional[dict]:
        """Get a user by ID."""
        row = self.conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None
    
    def authenticate(self, username: str, password: str) -> Optional[dict]:
        """Authenticate a user by username and password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        row = self.conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, password_hash),
        ).fetchone()
        return dict(row) if row else None
    
    def close(self):
        """Close the database connection."""
        self.conn.close()


class UserService:
    """Business logic for user operations."""
    
    def __init__(self, db: Database):
        self.db = db
    
    def register(self, username: str, email: str, password: str) -> dict:
        """Register a new user."""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        user_id = self.db.create_user(username, email, password)
        return self.db.get_user(user_id)
    
    def login(self, username: str, password: str) -> Optional[dict]:
        """Authenticate and return user data."""
        return self.db.authenticate(username, password)
