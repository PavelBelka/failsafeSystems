import numpy as np

class Node:
    def __init__(self, name, index = None, destroyed = False, intensity = 0):
        self.name = name
        self.index = index
        self.destroyed = destroyed
        self.intensity = intensity

class Edge:
    def __init__(self, name, tuple_node, destroyed = False, length = 0, intensity = 0):
        self.name = name
        self.tuple_node = tuple_node
        self.destroyed = destroyed
        self.length = length
        self.intensity = intensity

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

    def get_edges(self):
        return self.edges

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

    def get_path_elements(self, paths):
        common_list = []
        for path in paths:
            path_list = []
            for item in path:
                element_list = [0, 0.0]
                index_path = path.index(item)
                element_list[0] = str(item)
                for node in self.nodes:
                    if node.index == item:
                        element_list[1] = node.intensity
                path_list.append(element_list.copy())
                if index_path == 0:
                    continue
                else:
                    node_a = path[index_path - 1]
                    node_b = path[index_path]
                    for edge in self.edges:
                        if (edge.tuple_node[0] == node_a and edge.tuple_node[1] == node_b) or \
                           (edge.tuple_node[1] == node_a and edge.tuple_node[0] == node_b):
                            path_list.insert(path_list.index(path_list[-1]), [f'{edge.tuple_node[0]}{edge.tuple_node[1]}', edge.intensity])
                            break
            common_list.append(path_list)
        return common_list
