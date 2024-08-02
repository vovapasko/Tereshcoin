import hashlib
import json
import time

import random
from json import JSONEncoder


def generate_hash(input_string: str) -> str:
    """
    Generates a SHA-256 hash of the input string.

    Args:
        input_string (str): The string to be hashed.

    Returns:
        str: The SHA-256 hash of the input string.
    """

    # Convert the input string to bytes and hash it twice.
    hashed_bytes = hashlib.sha256(input_string.encode()).digest()
    hashed_string = hashlib.sha256(hashed_bytes).hexdigest()

    return hashed_string

class Wallet:

    def __init__(self, address):
        self.address = address



class Transaction:
    def __init__(self, sender: Wallet, receiver: Wallet, when, amount):
        self.amount = amount
        self.when = when
        self.receiver = receiver
        self.sender = sender


class TransactionEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction):
            return o.__dict__
        return json.JSONEncoder.default(self, o)


trx1 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   '225e2708d54a4e8e0bfe2393dc2c28a32f2b3dd355706afb49363de7ddbf4c58',
                   1569761836.1613867,
                   150)
trx2 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   '150653f51df5e2aa0bda45b6f68ab4fd2c9c5620042baf6124bf5af302780115',
                   1569761836.1613867,
                   150)
trx3 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   'ec4006a60556d0f521847f487c4e0c57ee1a84982aa64a4fac2837fc71356d51',
                   1569761836.1613867,
                   150)
trx_list = [trx1, trx2, trx3]
