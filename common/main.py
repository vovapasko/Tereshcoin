from Node import Node
from merkle import get_hash, Transaction, MerkleTree

address = get_hash("Vova")
nodeV = Node(address)
chain = nodeV.get_chain_data

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
# merkle_t.createNodes()
root = merkle_t.getRootHash()
print(f"root - {root}")
print(f"right - {merkle_t.getRootElement(merkle_t.nodes, []).getRightChild()}")
print(f"left - {merkle_t.getRootElement(merkle_t.nodes, []).getLeftChild()}")