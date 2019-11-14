import os
import pickle
import socket
import time

from _datetime import datetime
import json
from concurrent.futures import thread
from threading import Thread

from merkle import Transaction, get_hash


class Node:
    def __init__(self, new_address):
        self.wallet_address = new_address
        self.node_chain_filename = str(new_address) + ".txt"
        self.chain_data = self.getChainData()
        self.address = socket.gethostname()
        self.port = 1234
        self.socket = self.initSocket()

    def initSocket(self):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM makes this a UDP socket
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpSocket.bind((self.address, self.port))
        udpSocket.settimeout(1)
        return udpSocket

    @property
    def get_chain_data(self):
        return self.chain_data

    @property
    def get_address(self):
        return self.wallet_address

    def getChainData(self):
        try:
            with open(self.node_chain_filename) as f:
                chain = json.load(f)
        except FileNotFoundError:
            chain = None
        return chain

    def send_coins(self, addressTo, amountCoins):
        if amountCoins > self.get_balance():
            raise Exception("Impossible to send coins. It is more than your balance")
        new_trx = Transaction(self.wallet_address, addressTo, time.time(), amountCoins)
        serialized_new_trx = pickle.dumps(new_trx)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.address, self.port))
        s.send(serialized_new_trx)
        s.close()

    def get_balance(self):
        money_in, money_out = 0, 0
        for i in range(len(self.chain_data)):
            for transaction in self.chain_data[i]["transactions"]:
                if transaction['moneyWho'] == self.wallet_address:
                    money_in += transaction['amount']
                if transaction['moneyFrom'] == self.wallet_address:
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

    def thread_listen(self):
        BUFFER_SIZE = 1024
        while True:
            try:
                data, from_addr = self.socket.recvfrom(BUFFER_SIZE)
                print(f'Received data from {from_addr}')
                # check data if it's sent from this same instance
                with open(self.node_chain_filename, 'a+') as file:
                    file.write(f'New data from {from_addr}:\n')
                    file.write(f'{data.decode()}\n')
                    file.flush()
                    os.fsync(file.fileno())
            except socket.timeout:  # happens on timeout, needed to not block on recvfrom
                pass  # generally, this is not needed, daemon threads end when program ends

    def send_message_to_nodes(self):
        header = "NODE_MAIN_INFO"
        _from = self.wallet_address
        message = "I am online!"
        json_message = {"header": header, "from": _from, "message": message}
        serialized_message = pickle.dumps(json_message)
        self.socket.sendto(serialized_message, (self.address, self.port))

    def start(self):
        listen_thread = Thread(target=self.thread_listen, daemon=True)
        listen_thread.start()

        self.send_message_to_nodes()
