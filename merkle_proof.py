import json

import credentials
from Node.Node import Node
from merkle import get_hash, Transaction, MerkleTree

with open(credentials.filename) as f:
    chain = json.load(f)

first_transactions = chain[0]['transactions']
trx_lst = []
for trans in first_transactions:
    a = trans['moneyFrom']
    b = trans['moneyWho']
    c = trans['when']
    d = trans['amount']
    new_Tx = Transaction(trans['moneyFrom'], trans['moneyWho'], trans['when'], trans['amount'])
    trx_lst.append(new_Tx)
merkle_t = MerkleTree(trx_lst)
print(merkle_t.getRootHash())

trx_to_proof = Transaction("14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1",
                           "225e2708d54a4e8e0bfe2393dc2c28a32f2b3dd355706afb49363de7ddbf4c58",
                           1571866523.0888188,
                           150)
merkle_t.proveTransaction(trx_to_proof.__hash__())

