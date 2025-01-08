import hashlib
import os
import mongoengine as me


def salt_hash_password(password: str, salt_bytes: int=15) -> dict:
    """
    password: Password to hash
    salt_bytes: Number of bytes to use from the salt for extra layer of security. Default is 15.
    """

    # Generate salt
    salt = os.urandom(16)

    # Combine salt and password
    salted_password = salt[:salt_bytes] + password.encode('utf-8')

    # Hash the salted password
    hash_digest = hashlib.sha256(salted_password).hexdigest()

    return {
        "salt": salt.hex(),
        "hash": hash_digest
    }


def verify_password(password: str, db_salt: str, db_hash: str, salt_bytes: int=15) -> bool:
    """
    password: Password to verify
    db_salt: Salt stored in the database in hexadecimal
    db_hash: Hash stored in the database in hexadecimal
    salt_bytes: Number of bytes to use from the salt for extra layer of security. Default is 15.
    """

    salt = bytes.fromhex(db_salt)

    # Combine salt and password
    salted_password = salt[:salt_bytes] + password.encode('utf-8')

    # Hash the salted password
    hash_digest = hashlib.sha256(salted_password).hexdigest()

    return hash_digest == db_hash