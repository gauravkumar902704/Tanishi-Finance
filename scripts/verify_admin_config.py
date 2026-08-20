"""Verify the .env has a valid bcrypt admin password hash without displaying secrets."""
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('ADMIN_USERNAME', '')
password_hash = os.getenv('ADMIN_PASSWORD_HASH', '').encode()
try:
    valid_hash = password_hash.startswith((b'$2a$', b'$2b$', b'$2y$')) and len(password_hash) == 60
    if valid_hash:
        bcrypt.checkpw(b'format-check-only', password_hash)
except ValueError:
    valid_hash = False
print('Admin username configured:', bool(username))
print('Bcrypt password hash valid:', valid_hash)
