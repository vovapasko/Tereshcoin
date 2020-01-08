import os
import pickle
import socket
import time

import json
import traceback
from datetime import datetime
from pathlib import Path
from threading import Thread

import tools
from merkle import Transaction, get_hash
from tools import functions


class Node:
    def __init__(self, new_address):
        self.wallet_address = new_address
        self.node_chain_filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + "data" + "\\" + str(
            new_address) + ".txt"
        self.node_info_filename = os.path.dirname(os.path.abspath(__file__)) + "\\" + "nodes" + "\\" + str(
            new_address) + ".txt"
        self.chain_data = self.getChainData()
        self.address = '<broadcast>'
        self.port = 1234
        self.socket = self.initSocket()
        self.node_data = None
        self.time_start_online = datetime.now().timestamp()

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

    def writeChainData(self, data):
        try:
            with open(self.node_chain_filename, "a") as f:
                str_data = json.dumps(data)
                f.write(str_data)
        except FileNotFoundError:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_to_create = dir_path + "\\" + "data"
            os.makedirs(dir_to_create)
            file = open(self.node_chain_filename, "w")
            file.write(data)
            file.close()


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
        BUFFER_SIZE = 10240
        while True:
            try:
                data, from_addr = self.socket.recvfrom(BUFFER_SIZE)
                # check data if it's sent from this same instance
                deserealizedJson = pickle.loads(data)
                message_header = deserealizedJson["header"]
                try:
                    call_func = functions[message_header]
                except KeyError:
                    print("If you get this Exception, you forgot to create key for your function and header")
                    traceback.print_exc()
                deserealizedJson["from_ip_address"] = from_addr
                deserealizedJson["port_listened"] = self.port
                # todo send to this function only node information, message_from and deserialized json message
                res = call_func(node=self, message=deserealizedJson)
                # todo think how to remaster this spaghetti code
                if message_header == tools.node_connected_to_network and self.get_nodes_online() != 0:  # means that older node sees a new node and sends back respond
                    header = tools.from_older_node_id
                    _from = self.wallet_address
                    message = "Hello from older node!"
                    time_online = datetime.now().timestamp() - self.time_start_online
                    # todo send to this function only node information and deserialized json message
                    json_message = tools.format_json_message(header=header, _from=_from, message=message)
                    self.send_message_to_nodes(json_message)
            except socket.timeout:  # happens on timeout, needed to not block on recvfrom
                pass  # generally, this is not needed, daemon threads end when program ends

    def send_me_online(self):
        header = tools.node_connected_to_network
        _from = self.wallet_address
        message = "I am online!"
        json_message = tools.format_json_message(header=header, _from=_from, message=message)
        self.send_message_to_nodes(json_message)
        my_file = Path(self.node_chain_filename)
        if not my_file.is_file():
            file = open(self.node_chain_filename, "w")
            file.close()

    def send_message_to_nodes(self, json_message):
        serialized_message = pickle.dumps(json_message)
        self.socket.sendto(serialized_message, (self.address, self.port))

    def get_nodes_online(self):
        self.node_data = self.getNodeData()
        if self.node_data:
            return len(self.node_data)
        return 0

    # todo import this method from tools
    def getNodeData(self):
        try:
            file = open(self.node_info_filename, "r")
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

    def ask_for_data(self):
        nodes_online = self.get_nodes_online()
        if nodes_online > 0:
            nodes = self.getNodeData()
            self.send_give_data_message(nodes)
        else:
            print("I am alone in this world...")
        pass

    def send_give_data_message(self, nodes):
        header = tools.node_request_data
        _from = self.wallet_address
        message = "Give me a data"
        json_message = tools.format_json_message(header=header, _from=_from, message=message)
        self.send_message_to_nodes(json_message)

    def start(self):
        try:
            open(self.node_info_filename, "w").close()  # the log file must be empty before node goes online
        except FileNotFoundError:
            # means that file with nodes data doesn't exist and we need to create it
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_to_create = dir_path + "\\" + "nodes"
            os.makedirs(dir_to_create)
            file = open(self.node_info_filename, "w")
            file.close()
        listen_thread = Thread(target=self.thread_listen, daemon=True)
        listen_thread.start()
        self.send_me_online()
        # because writing the data about available nodes to the file could not be finished so we need some pause for it
        time.sleep(1)
        self.ask_for_data()
        while True:
            time.sleep(2)
            self.node_data = self.getNodeData()
            print("Node " + self.wallet_address + " is here!")
            print("Nodes online - " + str(self.get_nodes_online()))
            print("List of nodes: ")
            print(self.node_data)
            print("///////////")
