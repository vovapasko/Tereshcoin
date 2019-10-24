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
                           "ec4006a60556d0f521847f487c4e0c57ee1a84982aa64a4fac2837fc71356d51",
                           1571866523.0888188,
                           150)
trx_hash = trx_to_proof.__hash__()
proof = merkle_t.proveTransaction(trx_hash)

address = get_hash("Vova")
nodeV = Node(address)
nodeV.checkProof(trx_hash, proof, "77d248487a6a13241aa6cfd2ce19154ce245772fd5b3986213be005a9881201e")
