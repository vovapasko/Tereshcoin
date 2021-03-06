import pickle
import socket
import time

from _datetime import datetime
import json

from credentials import filename
from merkle import Transaction


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
        file = open(self.chain_file, mode="r")
        str = file.read()
        chain = []
        jsons = str.split("}{")
        if len(jsons) == 1:
            jso = json.loads(jsons[0])
            chain.append(jso)
            return chain
        for i in range(len(jsons)):
            if i == 0:
                jsons[i] += "}"
            elif i < len(jsons) - 1:
                jsons[i] = "{" + jsons[i] + "}"
            else:
                jsons[i] = "{" + jsons[i]
            chain.append(json.loads(jsons[i]))
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

#
# n = Node("B0")
# balance = n.get_balance()
# print(balance)
