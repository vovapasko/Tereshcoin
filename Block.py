import time

from merkle import get_hash


class Block:
    def __init__(self, previous_block, merkleRoot, transactions):
        self.timestamp = time.time()
        self.nonce = 0
        self.previous_block = previous_block
        # self.target = '0x00000000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.target = '0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        self.merkleRoot = merkleRoot
        self.block_hash = self.__hash__()
        self.transactions = transactions

    def __hash__(self):
        return get_hash(
            str(self.previous_block) + str(self.timestamp) + str(self.nonce) + str(self.target) + str(self.merkleRoot))
