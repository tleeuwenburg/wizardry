import builtins
from unittest.mock import patch

import matplotlib.pyplot as plt
import networkx as nx

import warnings
warnings.filterwarnings("ignore")

class Node():

    def __init__(self, nxgraph, master, name):

        self.master = master
        self.name = name

        self.nxg = nxgraph
        self.nxg.add_node(name)

    def __gt__(self, other):

        valid = True

        # If mutable, add an edge and return True
        if self.master.mutable:
            edge = self.nxg.add_edge(self.name, other.name)
            # self.master.edges.append(edge)

        # If immutable, return True if there is a matching edge
        if not self.master.mutable:
            raise Exception("Not implemented yet")

        return valid

    # def __lt__(self, other):
    #     pass
    #
    # def __eq__(self, other):
    #     pass

class graph():

    def __init__(self):
        self.nxg = nx.Graph()
        self.mutable = False

    def node(self, name):
        n = Node(self.nxg, self, name)
        return n

    def draw(self):
        nx.draw(self.nxg, with_labels=True, node_color="#aaafff")
        plt.show()


    def __enter__(self):
        self.mutable = True

    def __exit__(self, *args):
        self.mutable = False
