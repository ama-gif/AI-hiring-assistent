import re

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone):
    """Validate phone number format."""
    # Allow +country code and various formats
    pattern = r'^\+?1?\d{9,15}$'
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    return bool(re.match(pattern, phone))