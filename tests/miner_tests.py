import unittest
from common.merkle import Transaction, Wallet
from miner.Miner import Miner


class MinerTestCase(unittest.TestCase):
    def setUp(self):
        self.miner = Miner('test_address')
        
    def test_miner_initialization(self):
        miner = Miner(address='miner_address')
        assert miner.address == 'miner_address'
        assert miner.target == '0x00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF'
        assert miner.nonce == 0
    
    def test_mine(self):
        miner = Miner(address='miner_address')
        transactions = [
            Transaction(sender=Wallet('Jake'), receiver=Wallet('Martha'), when=123456, amount=100),
            Transaction(sender=Wallet('Andrew'), receiver=Wallet('Tristan'), when=123456, amount=200),
            Transaction(sender=Wallet('Donald'), receiver=Wallet('Joe'), when=123456, amount=300),
            Transaction(sender=Wallet('Olaf'), receiver=Wallet('Robert'), when=123456, amount=400),
            ]
        mined_block = miner.mine(transactions)
        assert mined_block is not None
        # Add more assertions based on the mining process