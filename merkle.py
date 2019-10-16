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
        return get_hash(self.root.leftChildHash + self.root.rightChildHash)

    def getRootElement(self, nodes, roots):
        if len(roots) == 1 and len(nodes) == 0:
            return roots[0]
        if len(nodes) == 0:
            return self.getRootElement(roots, [])
        if len(nodes) == 1:
            roots.append(MerkleNode(nodes[0].__hash__(), nodes[0].__hash__()))
            return self.getRootElement(roots, [])
        else:
            roots.append(MerkleNode(nodes[0].__hash__(), nodes[1].__hash__()))
            new_nodes = nodes[2:]
            return self.getRootElement(new_nodes, roots)

    def getRoot(self):
        root = self.getRootElement(self.nodes, [])
        return root

    # def printTree(self):
    #     root = self.getCHildTree(self.root)
    #

    def getCHildTree(self, root):
        left = root.getLeftChild()
        right = root.getRightChild()
        pass


class MerkleNode:
    def __init__(self, leftChild, rightChild):
        self.leftChildHash = leftChild
        self.rightChildHash = rightChild

    def getRoot(self):
        return get_hash(self.leftChildHash + self.rightChildHash)

    def getLeftChild(self):
        return self.leftChildHash

    def getRightChild(self):
        return self.rightChildHash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return get_hash(self.leftChildHash + self.rightChildHash)


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


trx1 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   '225e2708d54a4e8e0bfe2393dc2c28a32f2b3dd355706afb49363de7ddbf4c58',
                   1569761836.1613867,
                   150)
trx2 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   '150653f51df5e2aa0bda45b6f68ab4fd2c9c5620042baf6124bf5af302780115',
                   1569761836.1613867,
                   150)
trx3 = Transaction('14d6f42ada24c3c1a6b839a574fa1dc0c2629011fc732635635e6c6b78192fd1',
                   'ec4006a60556d0f521847f487c4e0c57ee1a84982aa64a4fac2837fc71356d51',
                   1569761836.1613867,
                   150)
trx_list = [trx1, trx2, trx3]
tree = MerkleTree(trx_list)
root = tree.getRoot()
left = root.getLeftChild()
right = root.getRightChild()
no_child = left.getLeftChild()