import pickle
import socket
import time

from _datetime import datetime
import json

from credentials import filename
from merkle import Transaction, get_hash


class Node:
    def __init__(self, new_address):
        self.address = new_address
        self.chain_file = filename
        self.chain_data = self.getChainData()
        self.hostname = socket.gethostname()
        self.port = 1234

    @property
    def get_chain_data(self):
        return self.chain_data

    @property
    def get_address(self):
        return self.address

    def getChainData(self):
        with open(filename) as f:
            chain = json.load(f)
        return chain

    def send_coins(self, addressTo, amountCoins):
        if amountCoins > self.get_balance():
            raise Exception("Impossible to send coins. It is more than your balance")
        new_trx = Transaction(self.address, addressTo, time.time(), amountCoins)
        serialized_new_trx = pickle.dumps(new_trx)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.hostname, self.port))
        s.send(serialized_new_trx)
        s.close()

    def get_balance(self):
        money_in, money_out = 0, 0
        for i in range(len(self.chain_data)):
            for transaction in self.chain_data[i]["transactions"]:
                if transaction['moneyWho'] == self.address:
                    money_in += transaction['amount']
                if transaction['moneyFrom'] == self.address:
                    money_out += transaction['amount']
        return money_in - money_out

    def check_proof(self, trx_to_check, proof, real_merkle_root_hash):
        '''
        real_merkle_root_hash - real hash from real block 
        '''        
        real_root = real_merkle_root_hash
        root_from_proof = self.get_root(trx_to_check, proof)
        return real_root == root_from_proof

    def get_root(self, node_hash, proof):
        if len(proof) == 0:
            return node_hash
        proof_hash_position = proof[0].get('position')
        proof_hash_value = proof[0].get('value')
        # next line solves hash commutative problem when hash(a) + hash(b) != hash(b) + hash(a) by
        # determining the way of addition by the position of hash in initial Merkle tree 
        new_hash = get_hash(node_hash + proof_hash_value) if proof_hash_position == 'right' else get_hash(proof_hash_value + node_hash)
        return self.get_root(new_hash, proof[1:])
