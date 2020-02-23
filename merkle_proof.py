import json

import credentials
from Node.Node import Node
from merkle import get_hash, Transaction, MerkleTree
from Block import Block

with open(credentials.filename) as f:
    chain = json.load(f)

first_transactions = chain[0]['transactions']
trx1 = Transaction('A', 'B', 1571866523.0888188, 150)
trx2 = Transaction('C', 'D', 1571866523.0888188, 150)
trx3 = Transaction('E', 'F', 1571866523.0888188, 150)
trx4 = Transaction('G', 'H', 1571866523.0888188, 150)
trx_lst = [trx1, trx2, trx3, trx4]


merkle_t = MerkleTree(trx_lst)
print(merkle_t.getRootHash())
trx_to_proof = Transaction('E', 'F', 1571866523.0888188, 150)
trx_hash = trx_to_proof.__hash__()
proof = merkle_t.getTransactionProof(trx_hash)

address = get_hash("Vova")
nodeV = Node(address)
res = nodeV.check_proof(trx_hash, proof, merkle_t.getRootHash())
print(res)