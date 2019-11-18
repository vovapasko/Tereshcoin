from threading import Thread

from Node_dir.Node import Node

nodeP = Node("Petya")
threadP = Thread(target=nodeP.start).start()
