import pickle
import random
import socket
import time
import json
import os

import credentials
from Block import Block
from merkle import Transaction, MerkleTree, get_hash, TransactionEncoder


def lessThanTarget(hash, target):
    a = int(hash, 16)
    b = int(target, 16)
    return int(hash, 16) < int(target, 16)


def writeToChain(block):
    # convert to json block in dict form, and in order to serialize Transaction class use TransactionEncoder
    with open(filename, mode="a") as file:
        new_json = json.dumps(block.__dict__, cls=TransactionEncoder, indent=4)
        file.write(new_json)


def mine(block):
    solution_found = False

    block.nonce = 0

    target = str(block.target)

    while not solution_found:
        new_hash = block.__hash__()
        print("Block hash", new_hash)
        print("target - ", int(target, 16))
        print("Number - ", int(new_hash, 16))
        print("Nonce = ", block.nonce)
        print('Is the block hash less than the target?')
        solution_found = lessThanTarget(new_hash, target)
        print(solution_found)
        print("-------------")
        if not solution_found:
            block.nonce += 1

    writeToChain(block)


filename = credentials.filename
trx_in_block = 3
trx_list = []
# for i in range(trx_in_block):
#     trx = Transaction("B" + str(i), "A" + str(i), time.time(), random.random() * 50)
#     trx_list.append(trx)
# tree = MerkleTree(trx_list)
# tree.createNodes()
# root = tree.getRootHash()

# genesis_block = Block("0", root, trx_list)
#
# mine(genesis_block)
amountNodes = 5


def get_previous_hash(filename):
    # means it was no previous block in chain
    file = open(filename, mode="r")
    str = file.read()
    chain = []
    jsons = str.split("}{")
    if len(jsons) == 1:
        jso = json.loads(jsons[0])
        chain.append(jso)
        return chain[0]["block_hash"]
    for i in range(len(jsons)):
        if i == 0:
            jsons[i] += "}"
        elif i < len(jsons) - 1:
            jsons[i] = "{" + jsons[i] + "}"
        else:
            jsons[i] = "{" + jsons[i]
        chain.append(json.loads(jsons[i]))
    return chain[-1]["block_hash"]


def create_new_block(trx_list):
    tree = MerkleTree(trx_list)
    previous_hash = get_previous_hash(filename)
    new_block = Block(previous_hash, tree.getRootHash(), trx_list)
    mine(new_block)


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(amountNodes)
    while True:
        clientNodeSocket, nodeAddress = s.accept()
        print(f"Data from {nodeAddress} has been received.")
        new_msg = clientNodeSocket.recv(1024)
        trx = pickle.loads(new_msg)
        trx_list.append(trx)
        print(f"Have {len(trx_list)} transactions. Need {trx_in_block - len(trx_list)} more to start mining")
        if len(trx_list) == trx_in_block:
            create_new_block(trx_list)


if __name__ == '__main__':
    start()
