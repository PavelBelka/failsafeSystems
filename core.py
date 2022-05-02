import networkx as nx
from MainWindow import MainWindow
from Graph import Graph
import gc

class Core:
    def __init__(self, model, settings):
        self.settings = settings
        self.model = model
        self.view = MainWindow(self)
        self.view.set_settings(self.settings.get_settings())
        self.graph = None

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
        g = nx.from_numpy_matrix(self.graph.get_matrix(), create_using=nx.MultiGraph)
        self.view.drawGraph(g, dict_labels)
        self.view.output_table_nodes(self.graph.get_nodes())

    def handle_graph_delete_button_clicked(self):
        del self.graph
        gc.collect()
        self.view.clearGraph()

