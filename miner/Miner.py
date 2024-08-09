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
        self.zeroes_amount = 62
        self.nonce = 0
        self.previous_block_hash = self.__get_previous_block_hash()

    def __get_previous_block_hash(self):
        # lookup for previous hash in blockchain otherwise return zero hash
        return '0x0000000000000000000000000000000000000000000000000000000000000000'
        
    def mine(self, transactions: List[Transaction]) -> Block:
        merkle_root = MerkleTree([transaction.__hash__() for transaction in transactions]).root.hex()
        new_block = Block(self.previous_block_hash, merkle_root, transactions)
        i = 1
        while not self.__less_than_target(new_block.__hash__(), new_block.target):
            self.__report_status(new_block, i)
            new_block.iterate_nonce()
            i += 1
        self.__report_status(new_block, i)
        return new_block

    def __less_than_target(self, old_hash: str, target: str):
        return int(old_hash, 16) < int(target, 16)

    def __report_status(self, block: Block, iteration: int = 0):
        print(f'-------Iteration: {iteration}-------')
        print('HEX Target is:', block.target, sep='\n')
        print('INT Target is:', int(block.target, 16), sep='\n')
        print('HEX Old Hash is:', block.__hash__(), sep='\n')
        print('INT Old Hash is:', int(block.__hash__(), 16), sep='\n')
        print(f'Block hash less than target: {self.__less_than_target(block.__hash__(), block.target)}')
        print(f'Nonce: {block.nonce}')
