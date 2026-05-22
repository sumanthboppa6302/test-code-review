"""Utility functions for the application."""


def validate_email(email: str) -> bool:
    """Check if an email address is valid."""
    return "@" in email and "." in email.split("@")[1]


def format_username(name: str) -> str:
    """Format a username to lowercase with no spaces."""
    return name.lower().strip().replace(" ", "_")


def calculate_password_strength(password: str) -> str:
    """Return password strength rating."""
    if len(password) < 8:
        return "weak"
    elif len(password) < 12:
        return "medium"
    else:
        return "strong"
