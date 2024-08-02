import datetime
import time

import miner.Miner as Miner
from Block import Block
from merkle import Transaction, get_hash, MerkleTree

'''
    Mining of genesis block
'''

# creator_coins = get_hash("Creator")
# first_address = get_hash("Vova")
# second_address = get_hash("Alice")
# third_address = get_hash("Bob")
#
# trx1 = Transaction(creator_coins, first_address, time.time(), 150)
# trx2 = Transaction(creator_coins, second_address, time.time(), 150)
# trx3 = Transaction(creator_coins, third_address, time.time(), 150)
# trx_list = [trx1, trx2, trx3]
# tree = MerkleTree(trx_list)
#
# genesis_block = Block("0", tree.getRootHash(), trx_list)
# Miner.mine(genesis_block)


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
tree = MerkleTree(trx_list)
num = tree.getRootHash()
