from threading import Thread

from Node_dir.Node import Node

nodeJ = Node("John")
threadJ = Thread(target=nodeJ.start).start()
