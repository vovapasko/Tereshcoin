import hashlib
import json
import time

import random
from json import JSONEncoder


def get_hash(string):
    return hashlib.sha256(hashlib.sha256(string.encode("utf-8")).hexdigest().encode('utf-8')).hexdigest()


class MerkleTree:
    def __init__(self, transactions):
        self.transactions = sorted(transactions, key=lambda trx: trx.when)
        self.nodes = []
        self.createNodes()
        self.root = self.getRoot()

    def createNodes(self):
        if len(self.transactions) == 1:
            self.nodes.append(MerkleNode(self.transactions[0].__hash__(), self.transactions[0].__hash__()))
        else:
            for i in range(0, len(self.transactions), 2):
                if i % 2 == 0 and i == len(self.transactions) - 1:
                    self.nodes.append(MerkleNode(self.transactions[i].__hash__(), self.transactions[i].__hash__()))
                else:
                    self.nodes.append(MerkleNode(self.transactions[i].__hash__(), self.transactions[i + 1].__hash__()))

    def getRootHash(self):
        return self.root.my_hash

    def getRootElement(self, nodes, roots):
        if len(roots) == 1 and len(nodes) == 0:
            return roots[0]
        if len(nodes) == 0:
            return self.getRootElement(roots, [])
        if len(nodes) == 1:
            roots.append(MerkleNode(nodes[0], nodes[0]))
            return self.getRootElement(roots, [])
        else:
            roots.append(MerkleNode(nodes[0], nodes[1]))
            new_nodes = nodes[2:]
            return self.getRootElement(new_nodes, roots)

    def getRoot(self):
        root = self.getRootElement(self.nodes, [])
        return root

    def printTree(self, root):
        new_root = root
        left = new_root.getLeftChild()
        right = new_root.getRightChild()
        print(f"Root - {new_root}. It's hash - {new_root.__hash__()}")
        print(f"Right - {right}. It's hash - {right.__hash__()}")
        print(f"Left - {left}. It's hash - {left.__hash__()}")
        print("---------------")
        if isinstance(left, str) and isinstance(right, str):
            return
        self.printTree(left)
        self.printTree(right)

    def hasTransaction(self, id_transaction_to_check):

        return False


class MerkleNode:
    def __init__(self, leftChild, rightChild):
        self.leftChildHash = leftChild
        self.rightChildHash = rightChild
        self.my_hash = self.__hash__()

    def getLeftChild(self):
        return self.leftChildHash

    def getRightChild(self):
        return self.rightChildHash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        if isinstance(self.leftChildHash, str) and isinstance(self.rightChildHash, str):
            return get_hash(self.leftChildHash + self.rightChildHash)
        else:
            return get_hash(self.leftChildHash.my_hash + self.rightChildHash.my_hash)


class Transaction:
    def __init__(self, moneyFrom, moneyWho, when, amount):
        self.amount = amount
        self.when = when
        self.moneyWho = moneyWho
        self.moneyFrom = moneyFrom

    def __eq__(self, other):
        return get_hash(self.moneyWho + self.moneyFrom + str(self.when) + str(self.amount)) == \
               get_hash(other.moneyWho + other.moneyFrom + str(other.when) + str(other.amount))

    def __hash__(self):
        a = self.moneyWho
        b = self.moneyFrom
        c = hash(self.when)
        d = hash(self.amount)
        shastr = get_hash(a + b + str(c) + str(d))
        return shastr


class TransactionEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Transaction):
            return o.__dict__
        return json.JSONEncoder.default(self, o)