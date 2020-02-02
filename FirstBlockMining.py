import datetime
import time

from Block import Block
from Miner_dir import Miner
from merkle import Transaction, get_hash, MerkleTree

'''
    Mining of genesis block
'''

creator_coins = get_hash("Creator")
first_address = get_hash("Vova")
second_address = get_hash("Alice")
third_address = get_hash("Bob")

trx1 = Transaction(creator_coins, first_address, time.time(), 150)
trx2 = Transaction(creator_coins, second_address, time.time(), 150)
trx3 = Transaction(creator_coins, third_address, time.time(), 150)
trx_list = [trx1, trx2, trx3]
tree = MerkleTree(trx_list)

genesis_block = Block("0", tree.getRootHash(), trx_list)
Miner.mine(genesis_block)
