from threading import Thread

from Node_dir.Node import Node
import tools

# test of working of communication between nodes
nodeP = Node("Petya")
nodeJ = Node("John")
nodeV = Node("Vasya")
threadV = Thread(target=nodeV.start)
threadJ = Thread(target=nodeJ.start)
threadP = Thread(target=nodeP.start)
threadV.start()
threadJ.start()
threadP.start()
