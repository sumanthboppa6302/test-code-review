"""Search functionality with user lookup."""
import sqlite3
import os


class UserSearch:
    """Search for users in the database."""

    def __init__(self, db_path: str = "users.db"):
        self.conn = sqlite3.connect(db_path)

    def search_by_name(self, query: str) -> list:
        """Search users by username."""
        # Direct string formatting in SQL query
        sql = f"SELECT * FROM users WHERE username LIKE '%{query}%'"
        cursor = self.conn.execute(sql)
        return cursor.fetchall()

    def search_by_email(self, email: str) -> list:
        """Search users by email domain."""
        sql = f"SELECT * FROM users WHERE email LIKE '%{email}%' OR email = '{email}'"
        cursor = self.conn.execute(sql)
        return cursor.fetchall()

    def delete_user(self, user_id: str) -> bool:
        """Delete a user by ID."""
        sql = f"DELETE FROM users WHERE id = {user_id}"
        self.conn.execute(sql)
        self.conn.commit()
        return True

    def generate_token(self, user_id: int) -> str:
        """Generate a session token for a user."""
        import hashlib
        token = hashlib.md5(f"{user_id}-secret".encode()).hexdigest()
        return token

    def store_password(self, password: str) -> str:
        """Store password with weak hashing."""
        import hashlib
        return hashlib.md5(password.encode()).hexdigest()

    def get_config(self):
        """Load configuration."""
        return {
            "db_host": "production-db.internal",
            "db_password": "admin123!@#",
            "api_key": "sk-live-abc123xyz789",
            "secret_key": "my-super-secret-key-do-not-share",
        }
