import networkx as nx
from MainWindow import MainWindow
from Graph import Graph, Edge
from simulation import Simulation
import gc

class Core:
    def __init__(self, settings):
        self.settings = settings
        self.view = MainWindow(self)
        self.view.set_settings(self.settings.get_settings())
        self.graph = None
        self.network = None
        self.simulate = None

    def window_show(self):
        self.view.show()

    def handle_graph_create_button_clicked(self, topology):
        dict_labels = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J'}
        self.graph = Graph(10)
        if topology == "Полносвязанная":
            self.graph.fully_connected_graph()
        elif topology == "Ячеистая":
            self.graph.cellular_graph()
        elif topology == "Звезда":
            self.graph.star_graph()
        elif topology == "Кольцо":
            self.graph.ring_graph()
        elif topology == "Древовидное":
            self.graph.tree_graph()
        self.network = nx.from_numpy_matrix(self.graph.get_matrix(), create_using=nx.MultiGraph)
        self.view.drawGraph(self.network, dict_labels)
        self.view.output_table_nodes(self.graph.get_nodes())
        self.view.output_table_edges(self.graph.get_edges(self.network))

    def handle_graph_delete_button_clicked(self):
        del self.graph
        gc.collect()
        self.view.clearGraph()

    def handle_save_settings_button_clicked(self, number_failure, number_repair, intensity, police_repair):
        self.settings.set_settings('settings.yaml', [number_failure, number_repair, intensity, police_repair])

    def handle_start_simulate_button_clicked(self, start_node, stop_node):
        settings = self.settings.get_settings()
        self.simulate = Simulation(self.network, settings[0], settings[1], settings[2], settings[2])
        del settings
        nodes = self.graph.get_nodes()
        node_a = None
        node_b = None
        list_edges = [Edge(item) for item in list(self.network.edges(data=False))]
        for node in nodes:
            if node.name == start_node:
                node_a = node.index
            elif node.name == stop_node:
                node_b = node.index
        self.simulate.start_simulation(node_a, node_b, list_edges, nodes)
        del list_edges
        del nodes
        del self.simulate
        gc.collect()