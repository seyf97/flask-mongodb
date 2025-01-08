from typing import Mapping, Any
from flask import Response
from bson import json_util
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


def set_fields(doc: me.Document, in_fields: dict, exclude_fields: list[str]) -> me.Document:
    """
    doc: Document to set fields
    in_fields: Fields to set in the document
    exclude_fields: Fields to exclude from the document. Excludes id by default.
    """

    # Default exclude id
    if exclude_fields is None:
        exclude_fields = ["id"]
    else:
        exclude_fields.append("id")

    doc_fields = list(set(doc._fields.keys()) - set(exclude_fields))

    # Iterate, raise exception if field not in document
    for field in in_fields:
        if field not in doc_fields:
            raise me.errors.FieldDoesNotExist(f"Field '{field}' is not valid")

        setattr(doc, field, in_fields[field])

    return doc