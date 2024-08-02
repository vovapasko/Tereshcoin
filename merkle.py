import json
from merkly.mtree import MerkleTree
from json import JSONEncoder
from hashlib import sha256

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
        return sha256(json.dumps(self, cls=TransactionEncoder).encode()).hexdigest()
    
class TransactionEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction) or isinstance(o, Wallet):
            return o.__dict__
        return json.JSONEncoder.default(self, o)

        
bobs_wallet = Wallet('Bob', '14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1')
alices_wallet = Wallet('Alice', '225e2708d54a4e8e0bfe2393dc2c28a32f2b3dd355706afb49363de7ddbf4c58')
james_wallet = Wallet('James', '150653f51df5e2aa0bda45b6f68ab4fd2c9c5620042baf6124bf5af302780115')

trx1 = Transaction(bobs_wallet,
                   alices_wallet,
                   1569761836.1613867,
                   150)
trx2 = Transaction(bobs_wallet,
                   james_wallet,
                   1569761836.1613867,
                   150)
trx3 = Transaction(bobs_wallet,
                   alices_wallet,
                   1569761836.1613867,
                   150)
trx_list = [trx1.__hash__(), trx2.__hash__(), trx3.__hash__()]

tree = MerkleTree(trx_list)
print(tree.raw_leaves)

proof = tree.proof(trx1.__hash__())
print(tree.verify(proof=proof, raw_leaf=trx1.__hash__()))
print(tree.verify(proof=proof, raw_leaf="trx2.__hash__()"))


