import numpy as np

class Node:
    def __init__(self, name, indexloc = None):
        self.name = name
        self.index = indexloc


class Graph:
    def __init__(self, num, nodes = None):
        self.matrix = np.zeros((num, num))
        self.nodes = nodes
        self.list_name = []
        if self.nodes is not None:
            for i in range(len(self.nodes)):
                self.nodes[i].index = i

    def generate_nodes(self, name_nodes: list):
        self.nodes = []
        for name in name_nodes:
            self.nodes.append(Node(name, name_nodes.index(name)))

    def connect_dual(self, connections: dict):
        for item in self.nodes:
            obj = connections.get(item.name)
            if obj is not None:
                for i in obj:
                    column = 0
                    for j in self.nodes:
                        if j.name == i:
                            column = j.index
                            break
                    self.matrix[item.index][column] = 1
                    self.matrix[column][item.index] = 1

    def get_matrix(self):
        return self.matrix

    def get_nodes(self):
        return self.nodes

    def fully_connected_graph(self):
        self.list_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        dict_edges = {
            'A': ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            'B': ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            'C': ['A', 'B', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
            'D': ['A', 'B', 'C', 'E', 'F', 'G', 'H', 'I', 'J'],
            'E': ['A', 'B', 'C', 'D', 'F', 'G', 'H', 'I', 'J'],
            'F': ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J'],
            'G': ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J'],
            'H': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'J'],
            'I': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J']
        }
        self.generate_nodes(self.list_name)
        self.connect_dual(dict_edges)

    def cellular_graph(self):
        self.list_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        dict_edges = {
            'A': ['B'],
            'B': ['C', 'D'],
            'C': ['G'],
            'D': ['E'],
            'E': ['F'],
            'F': ['B'],
            'G': ['H'],
            'H': ['I'],
            'I': ['J']
        }
        self.generate_nodes(self.list_name)
        self.connect_dual(dict_edges)

    def star_graph(self):
        self.list_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        dict_edges = {
            'A': ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']}
        self.generate_nodes(self.list_name)
        self.connect_dual(dict_edges)

    def ring_graph(self):
        self.list_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        dict_edges = {
            'A': ['B', 'J'],
            'B': ['C'],
            'C': ['D'],
            'D': ['E'],
            'E': ['F'],
            'F': ['G'],
            'G': ['H'],
            'H': ['I'],
            'I': ['J']
        }
        self.generate_nodes(self.list_name)
        self.connect_dual(dict_edges)

    def tree_graph(self):
        self.list_name = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        dict_edges = {
            'A': ['B'],
            'B': ['C', 'D'],
            'C': ['G'],
            'D': ['E'],
            'E': ['F'],
            'F': ['B'],
            'G': ['H'],
            'H': ['I'],
            'I': ['J']
        }
        self.generate_nodes(self.list_name)
        self.connect_dual(dict_edges)