"""Interactively set the admin password without showing it on screen."""
from getpass import getpass
from pathlib import Path
import bcrypt

root = Path(__file__).resolve().parents[1]
env_file = root / '.env'
if not env_file.exists():
    raise SystemExit('Create .env from .env.example first.')
first = getpass('New admin password: ')
second = getpass('Confirm password: ')
if len(first) < 12:
    raise SystemExit('Use at least 12 characters.')
if first != second:
    raise SystemExit('Passwords do not match.')
new_line = 'ADMIN_PASSWORD_HASH=' + bcrypt.hashpw(first.encode(), bcrypt.gensalt()).decode()
lines = env_file.read_text(encoding='utf-8').splitlines()
updated = [new_line if line.startswith('ADMIN_PASSWORD_HASH=') else line for line in lines]
env_file.write_text('\n'.join(updated) + '\n', encoding='utf-8')
print('Password updated. Restart the server before signing in.')
