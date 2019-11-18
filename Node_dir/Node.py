import os
import pickle
import socket
import time

import json
import traceback
from pathlib import Path
from threading import Thread

import tools
from merkle import Transaction, get_hash
from tools import functions


class Node:
    def __init__(self, new_address):
        self.wallet_address = new_address
        self.id = "NODE" + self.wallet_address
        self.node_chain_filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + "data" + "\\" + str(
            new_address) + ".txt"
        self.node_log_filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + "logs" + "\\" + str(
            new_address) + ".txt"
        self.chain_data = self.getChainData()
        self.address = '<broadcast>'
        self.port = 1234
        self.socket = self.initSocket()
        self.log_data = None

    def initSocket(self):
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # DGRAM makes this a UDP socket
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpSocket.bind(('', self.port))
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
                try:
                    chain = json.load(f)
                except json.decoder.JSONDecodeError:
                    chain = Node
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
                # check data if it's sent from this same instance
                deserealizedJson = pickle.loads(data)
                message_header = deserealizedJson["header"]
                message_from = deserealizedJson["_from"]
                try:
                    call_func = functions[message_header]
                except KeyError:
                    print("If you get this Exception, you forgot to create key for your function and header")
                    traceback.print_exc()
                deserealizedJson["from_ip_address"] = from_addr
                deserealizedJson["port_listened"] = self.port
                res = call_func(message_from=message_from, wallet_address=self.wallet_address,
                                deserealizedJson=deserealizedJson,
                                node_chain_filename=self.node_chain_filename,
                                node_log_filename=self.node_log_filename)
                # todo think how to remaster this spaghetti code
                if message_header == tools.node_connected_to_network and self.get_nodes_online() != 0:  # means that older node sees a new node and sends back respond
                    header = tools.from_older_node_id
                    _from = self.wallet_address
                    message = "Hello from older node!"
                    json_message = self.format_json_message(header=header, _from=_from, message=message)
                    self.send_message_to_nodes(json_message)
            except socket.timeout:  # happens on timeout, needed to not block on recvfrom
                pass  # generally, this is not needed, daemon threads end when program ends

    def send_me_online(self):
        header = tools.node_connected_to_network
        _from = self.wallet_address
        message = "I am online!"
        json_message = self.format_json_message(header=header, _from=_from, message=message)
        self.send_message_to_nodes(json_message)
        my_file = Path(self.node_chain_filename)
        if not my_file.is_file():
            file = open(self.node_chain_filename, "w")
            file.close()

    def send_message_to_nodes(self, json_message):
        serialized_message = pickle.dumps(json_message)
        self.socket.sendto(serialized_message, (self.address, self.port))

    def format_json_message(self, **data):
        new_json_message = {}
        for key, value in data.items():
            new_json_message[str(key)] = value
        return new_json_message

    def synchronise(self):
        pass

    def get_nodes_online(self):
        self.log_data = self.getLogData()
        if self.log_data:
            return len(self.log_data)
        return 0

    def getLogData(self):
        try:
            file = open(self.node_log_filename, "r")
            data_str = file.read().split("\n")
            if data_str[0] == '':  # means that there are no data in log file
                return None
            del data_str[-1]
            json_dict_arr = []
            for string in data_str:
                new_json = json.loads(string)
                json_dict_arr.append(new_json)
            return json_dict_arr
        except Exception:
            print(traceback.print_exc())
            return None

    def start(self):
        open(self.node_log_filename, "w").close()  # the log file must be empty before node goes online
        listen_thread = Thread(target=self.thread_listen, daemon=True)
        listen_thread.start()
        self.send_me_online()
        while True:
            time.sleep(2)
            self.log_data = self.getLogData()
            print("Node " + self.wallet_address + " is here!")
            print("Nodes online - " + str(self.get_nodes_online()))
            print("List of nodes: ")
            print(self.log_data)
            print("///////////")
