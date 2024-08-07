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
            Transaction(sender=Wallet('Jake', 'jake_address'), receiver=Wallet('Martha', 'martha_address'), when=123456, amount=100),
            Transaction(sender=Wallet('Andrew', 'andrew_address'), receiver=Wallet('Tristan', 'tristan_address'), when=123456, amount=200),
            Transaction(sender=Wallet('Donald', 'donald_address'), receiver=Wallet('Joe', 'joe_address'), when=123456, amount=300),
            Transaction(sender=Wallet('Olaf', 'olaf_address'), receiver=Wallet('Robert', 'robert_address'), when=123456, amount=400),
            ]
        mined_block = miner.mine(transactions)
        assert mined_block is not None
        # Add more assertions based on the mining process