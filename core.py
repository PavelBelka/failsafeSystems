import networkx as nx
import yaml
from MainWindow import MainWindow
from graph import Graph
from simulation import Simulation
from report import Report
from os import path
import gc

class Core:
    def __init__(self, settings):
        self.settings = settings
        self.view = MainWindow(self)
        self.view.set_settings(self.settings.get_settings())
        self.graph = None
        self.network = None
        self.simulate = None
        self.graphs_data = None
        self.report = Report()
        self.read_file_graphs()

    def window_show(self):
        self.view.show()

    def read_file_graphs(self):
        check_file_graphs = path.exists('graphs.yaml')
        if check_file_graphs is True:
            with open('graphs.yaml', 'r', encoding='utf-8') as file:
                self.graphs_data = yaml.load(file, Loader=yaml.FullLoader)
            self.view.output_list_graphs(list(self.graphs_data.keys()))
        else:
            pass

    def handle_graph_create_button_clicked(self, topology):
        self.graph = Graph(self.graphs_data[topology]['number_nodes'])
        self.graph.build_graph(self.graphs_data[topology])
        self.network = nx.from_numpy_matrix(self.graph.get_matrix(), create_using=nx.MultiGraph)
        self.view.drawGraph(self.network, self.graph.get_labels())
        self.view.output_table_nodes(self.graph.get_nodes())
        self.view.output_table_edges(self.graph.get_edges())

    def handle_graph_delete_button_clicked(self):
        self.view.clearChats()
        self.view.clearTables()
        del self.graph
        del self.network
        del self.simulate
        gc.collect()

    def handle_save_settings_button_clicked(self, number_failure, number_repair, intensity, police_repair):
        self.settings.set_settings('settings.yaml', [number_failure, number_repair, intensity, police_repair])

    def handle_start_simulate_button_clicked(self, start_node, stop_node, dict_nodes, dict_edges, intensity_connection, check):
        settings = self.settings.get_settings()
        self.simulate = Simulation(self.network, settings[0], settings[1], settings[2], settings[2], check, self.report)
        del settings
        nodes = self.graph.get_nodes()
        for node in nodes:
            node.intensity = float(dict_nodes[node.name]) * 1e-6
        node_a = None
        node_b = None
        edges = self.graph.get_edges()
        for edge in edges:
            edge.intensity = float(dict_edges[edge.name]) * float(intensity_connection) * 1e-6
        for node in nodes:
            if node.name == start_node:
                node_a = node.index
            elif node.name == stop_node:
                node_b = node.index
        paths = list(nx.all_simple_paths(self.network, node_a, node_b))
        data = self.graph.get_path_elements(paths)
        self.simulate.start_simulation(node_a, node_b, edges, nodes)
        self.view.output_probability_chart(self.report.output_probability(data))
        self.view.output_all_paths(paths, self.graph.get_labels())
        self.view.output_result(self.report.get_data_result())
        self.view.output_histogram(self.report.get_histogram_failure())
        del paths, edges, nodes
        del self.simulate
        gc.collect()