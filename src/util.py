from hashlib import sha256



def hash_function(input: bytes) -> str:
    return sha256(input).hexdigest()