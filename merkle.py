import json
from merkly.mtree import MerkleTree
from json import JSONEncoder
from util import hash_function


class Wallet:

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address


class Transaction:
    def __init__(self, sender: Wallet, receiver: Wallet, when, amount):
        self.amount = amount
        self.when = when
        self.receiver = receiver
        self.sender = sender

    def __hash__(self) -> str:
        return hash_function(json.dumps(self, cls=TransactionEncoder).encode())

class TransactionEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction) or isinstance(o, Wallet):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

