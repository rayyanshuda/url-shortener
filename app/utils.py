import secrets
import string

ALPHABET = string.ascii_letters + string.digits  # A–Z, a–z, 0–9

def generate_short_code(length: int = 6) -> str:
    #generate a random short code
    return ''.join(secrets.choice(ALPHABET) for _ in range(length))
