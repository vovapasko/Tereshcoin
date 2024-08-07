import time
from typing import List

from common.merkle import Transaction
from common.util import hash_function


class Block:
    
    @property
    def nonce(self):
        return self._nonce

    def iterate_nonce(self):
        self._nonce += 1

    def __init__(self, previous_block_hash: str, merkleRoot: str, transactions: List[Transaction]):    
        self.timestamp = time.time()
        self._nonce = 0 # private variable
        self.previous_block = previous_block_hash
        # self.target = '0x00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.target = '0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.merkleRoot = merkleRoot
        self.transactions = transactions
        self.block_hash = self.__hash__()

    def __hash__(self):
        return hash_function(
            (
                str(self.timestamp) + str(self.nonce) + str(self.previous_block) +
                str(self.merkleRoot) + str(self.transactions)
            ).encode()
        )
