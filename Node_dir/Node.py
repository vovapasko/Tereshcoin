import pickle
import socket
import time

from _datetime import datetime
import json

from Node_dir.node_credentials import filename
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

    def checkProof(self, trx_to_check, proof, block_hash):
        for block in self.chain_data:
            if block['block_hash'] == block_hash:
                my_block = block
        real_root = my_block['merkleRoot']
        root_from_proof = self.get_root(trx_to_check, proof)
        return real_root == root_from_proof

    def get_root(self, node_hash, proof):
        if len(proof) == 0:
            return node_hash
        new_hash = get_hash(node_hash + proof[0])
        return self.get_root(new_hash, proof[1:])

    def listen_miner(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.hostname, self.port))
        s.listen()
        minerSocket, minerAddress = s.accept()
        print(f"Data from {minerAddress} has been received.")
        new_msg = minerSocket.recv(1024)
        new_block = pickle.loads(new_msg)
        s.close()


if __name__ == '__main__':
    nodeV = Node(get_hash("Vova"))
    print(nodeV.get_balance())
    addressTo = get_hash("Paul")
    nodeV.send_coins(addressTo, 20)
    nodeV.listen_miner()
