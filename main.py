import json

# from Node import Node
# from merkle import get_hash, Transaction, MerkleTree
from Node.Node import Node
from merkle import get_hash

address = get_hash("Vova")
nodeV = Node(address)
chain = nodeV.get_chain_data
print(chain)
print(nodeV.get_balance())
