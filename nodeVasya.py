from threading import Thread

from Node_dir.Node import Node

nodeV = Node("Vasya")
threadJ = Thread(target=nodeV.start).start()
