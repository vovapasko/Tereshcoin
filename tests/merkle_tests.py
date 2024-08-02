
from src.merkle import Transaction, Wallet
from merkly.mtree import MerkleTree
import unittest
from src.merkle import Transaction, Wallet, MerkleTree

class MerkleTreeTestCase(unittest.TestCase):
    def setUp(self):
        self.bobs_wallet = Wallet('Bob', '14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1')
        self.alices_wallet = Wallet('Alice', '225e2708d54a4e8e0bfe2393dc2c28a32f2b3dd355706afb49363de7ddbf4c58')
        self.james_wallet = Wallet('James', '150653f51df5e2aa0bda45b6f68ab4fd2c9c5620042baf6124bf5af302780115')
        self.trx1 = Transaction(self.bobs_wallet, self.alices_wallet, 1569761836.1613867, 150)
        self.trx2 = Transaction(self.bobs_wallet, self.james_wallet, 1569761836.1613867, 150)
        self.trx3 = Transaction(self.bobs_wallet, self.alices_wallet, 1569761836.1613867, 150)
        self.trx_list = [self.trx1.__hash__(), self.trx2.__hash__(), self.trx3.__hash__()]
        self.tree = MerkleTree(self.trx_list)

    def test_raw_leaves(self):
        self.assertEqual(self.tree.raw_leaves, [self.trx1.__hash__(), self.trx2.__hash__(), self.trx3.__hash__()])

    def test_proof(self):
        proof = self.tree.proof(self.trx1.__hash__())
        self.assertEqual(self.tree.verify(proof=proof, raw_leaf=self.trx1.__hash__()), True)
        self.assertEqual(self.tree.verify(proof=proof, raw_leaf="trx2.__hash__()"), False)

