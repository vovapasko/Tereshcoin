import pickle
import random
import socket
import time
import json
import os
from pathlib import Path

import credentials
from Block import Block
from merkle import Transaction, MerkleTree, get_hash, TransactionEncoder


def lessThanTarget(hash, target):
    a = int(hash, 16)
    b = int(target, 16)
    return int(hash, 16) < int(target, 16)


def writeToChain(block):
    """
    This function gets the data from the block, converts it to json and save in chain(file) as the list pf jsons
    """
    # convert to json block in dict form, and in order to serialize Transaction class use TransactionEncoder
    exists = Path(filename).exists()
    with open(filename, mode="a") as file:
        new_json = json.dumps(block.__dict__, cls=TransactionEncoder, indent=4)
        if not exists:  # means that file doesn't exist and the symbol of the beginning of list should be written
            file.write('[')
        else:
            # next two lines delete the last symbol in file. It's made for further correct formatting of json
            file.seek(0, os.SEEK_END)
            file.seek(file.tell() - 1, os.SEEK_SET)
            file.truncate()
            file.write(',\n')
        file.write(new_json)
        file.write(']')


def mine(block):
    solution_found = False

    block.nonce = 0

    target = str(block.target)

    while not solution_found:
        new_hash = block.__hash__()
        print("Block hash", new_hash)
        print("target - ", int(target, 16))
        print("Block hash int - ", int(new_hash, 16))
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
amountNodes = 5


def get_previous_hash(filename):
    # means it was no previous block in chain
    with open(filename) as f:
        chain = json.load(f)
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
    print("Waiting for tasks")
    while True:
        clientNodeSocket, nodeAddress = s.accept()
        print(f"Data from {nodeAddress} has been received.")
        new_msg = clientNodeSocket.recv(1024)
        trx = pickle.loads(new_msg)
        trx_list.append(trx)
        print(f"Have {len(trx_list)} transactions. Need {trx_in_block - len(trx_list)} more to start mining")
        if len(trx_list) == trx_in_block:
            print("//////////////////////")
            print("Start mining")
            print("//////////////////////")
            create_new_block(trx_list)


if __name__ == '__main__':
    start()
