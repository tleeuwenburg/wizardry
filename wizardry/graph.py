import builtins
from unittest.mock import patch

import matplotlib.pyplot as plt
import networkx as nx

import warnings
warnings.filterwarnings("ignore")

class Edge():

    def __init__(self, master, a, b):
        self.a = a
        self.b = b
        self.id = master._edge_id()
        master.edges.append(self)

class Node():

    def __init__(self, nxgraph, master, name):

        self.master = master
        self.name = name

        self.nxg = nxgraph
        self.nxg.add_node(name)

    def __gt__(self, other):
        '''
        If in mutable mode, create an edge from self to other

        If in immutable mode, check if there is and edge from self to other

        @return True if the end state contains an edge from self to other
        @return False if there is not an edge from self to other
        '''

        valid = True

        # If mutable, add an edge and return True
        if self.master.mutable:
            self.nxg.add_edge(self.name, other.name)
            Edge(self.master, self, other)

        # If immutable, return True if there is a matching edge
        if not self.master.mutable:
            return self.master.has_edge(self, other)

        return valid

    def __lt__(self, other):
        '''
        Reverse of __gt__
        '''

        return Node.__gt__(other, self)

    def __eq__(self, other):
        '''
        In mutable mode, create a bidirectional edge between a and b

        @return true if there is a bidirectional edge between a and b
        '''

        eq1 = self > other
        eq2 = other > self
        both = eq1 and eq2

        return both


class graph():

    def __init__(self):
        self.nxg = nx.DiGraph()
        self.mutable = False

        self.edges = []
        self.edge_id = 0

    def _edge_id(self):
        self.edge_id += 1
        return self.edge_id

    def has_edge(self, a, b):
        for edge in self.edges:
            a_match = (edge.a.name == a.name)
            b_match = (edge.b.name == b.name)

            if a_match and b_match:
                return True

        return False

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
