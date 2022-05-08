import numpy as np

class Node:
    def __init__(self, name, indexloc = None, destroyed = False, intensity = 0):
        self.name = name
        self.index = indexloc
        self.destroyed = destroyed
        self.intensity = intensity

class Edge:
    def __init__(self, name, tuple_node, destroyed = False, length = 0):
        self.name = name
        self.tuple_node = tuple_node
        self.destroyed = destroyed
        self.length = length

class Graph:
    def __init__(self, num, nodes = None, edges = None):
        self.matrix = np.zeros((num, num))
        self.nodes = nodes
        self.edges = edges
        self.list_name = []
        if self.nodes is not None:
            for i in range(len(self.nodes)):
                self.nodes[i].index = i

    def generate_nodes(self, name_nodes: list):
        self.nodes = []
        for name in name_nodes:
            self.nodes.append(Node(name, name_nodes.index(name)))

    def connect_dual(self):
        for item in self.edges:
            self.matrix[item.tuple_node[0]][item.tuple_node[1]] = 1
            self.matrix[item.tuple_node[1]][item.tuple_node[0]] = 1

    def get_matrix(self):
        return self.matrix

    def get_nodes(self):
        return self.nodes

    def get_edges(self, network):
        common_list = []
        str_a = ''
        str_b = ''
        for edge in list(network.edges(data=False)):
            for node in self.nodes:
                if node.index == edge[0]:
                    str_a = node.name
                elif node.index == edge[1]:
                    str_b = node.name
            common_list.append(Edge(str_a + str_b, edge))
        return common_list

    def build_graph(self, data):
        self.nodes = []
        self.edges = []
        for node in data['Nodes']:
            self.nodes.append(Node(data['Nodes'][node]['name'], data['Nodes'][node]['index'], intensity=data['Nodes'][node]['intensity']))
        for edge in data['Edges']:
            self.edges.append(Edge(data['Edges'][edge]['name'], (data['Edges'][edge]['tuple_node'][0], data['Edges'][edge]['tuple_node'][1]),
                                   length=data['Edges'][edge]['length']))
        self.connect_dual()

    def get_labels(self):
        data = {}
        for item in self.nodes:
            data[item.index] = item.name
        return data