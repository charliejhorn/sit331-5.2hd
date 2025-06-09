import bcrypt

def hash_password(plain_password: str) -> str:
    """
    Hashes a plain text password using bcrypt.

    Args:
        plain_password (str): The password in plain text.

    Returns:
        str: The bcrypt hashed password, encoded as a string.
             This string can be safely stored in a database.
    """
    # bcrypt generates a salt automatically each time it hashes.
    # The default rounds (12) are generally a good balance for security and performance.
    # .encode('utf-8') is used to convert the string to bytes, as bcrypt works with bytes.
    hashed_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8') # Decode back to string for storage

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a bcrypt hashed password.

    Args:
        plain_password (str): The password provided by the user (in plain text).
        hashed_password (str): The bcrypt hashed password retrieved from storage.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
    """
    try:
        # bcrypt handles the salt extraction and hashing automatically during verification.
        # It's crucial to ensure both inputs are bytes.
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except ValueError:
        # This can happen if the hashed_password is not a valid bcrypt hash,
        # e.g., if it's too short or corrupted.
        print("Error: Hashed password is not in a valid bcrypt format.")
        return False