from threading import Thread

from Node_dir.Node import Node
import tools

# test of working of communication between nodes
nodeJ = Node("John")
nodeV = Node("Vasya")
# nodeP = Node("Petya")
threadJ = Thread(target=nodeJ.start).start()
threadV = Thread(target=nodeV.start).start()
# threadP = Thread(target=nodeP.start).start()
