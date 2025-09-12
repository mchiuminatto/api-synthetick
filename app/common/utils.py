from string import ascii_uppercase, digits
import random
import hashlib


def gen_random_alfa(size: int) -> str:
    """Generate a random alphanumeric ID of given size."""
    return "".join(random.choices(digits + ascii_uppercase, k=size))


def gen_using_hash(input_string: str, size: int) -> str:
    """Generate a unique ID using SHA-256 hash of the input string."""
    hash_object = hashlib.sha256(input_string.encode())
    hex_dig = hash_object.hexdigest()
    return hex_dig[:size]


