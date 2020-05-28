import json

# from Node import Node
# from merkle import get_hash, Transaction, MerkleTree
from Node import Node
from merkle import get_hash
from Miner import trx_in_block

nodeA = Node(get_hash("Alice"))
nodeB = Node(get_hash("Bob"))
nodeV = Node(get_hash("Vova"))

nodeA.send_coins(nodeB.address, 30)
nodeB.send_coins(nodeV.address, 30)
nodeA.send_coins(nodeV.address, 30)
