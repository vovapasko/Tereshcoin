import pickle
import random
import socket
import time
import json
import os
from typing import List

from common.Block import Block
from common.merkle import Transaction, MerkleTree


class Miner:

    def __init__(self, address):
        self.address = address
        self.target = '0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.nonce = 0
        self.previous_block_hash = self.__get_previous_block_hash()
    
    def __get_previous_block_hash(self):
        # lookup for previous hash in blockchain otherwise return zero hash
        return '0x0000000000000000000000000000000000000000000000000000000000000000'
        
    def mine(self, transactions: List[Transaction]) -> Block:
        merkle_root = MerkleTree(transactions).root.hex()
        new_block = Block(self.previous_block_hash, merkle_root, transactions)
        old_hash = new_block.__hash__()
        while int(old_hash, 16) < int(self.target, 16):
            new_block.iterate_nonce()
        return new_block
        
