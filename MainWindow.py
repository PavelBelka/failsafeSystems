from PyQt6.QtWidgets import QWidget, QTabWidget, QLabel, QPushButton, QMenuBar, QMenu, QGroupBox, QComboBox, \
    QMainWindow, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt6.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QAction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from networkx import draw, draw_networkx_labels, drawing


class MainWindow(QMainWindow):
    def __init__(self, presenter):
        super().__init__()

        self.presenter = presenter

        self.setFixedSize(960, 720)

        self.centralWidget = QWidget()
        self.centralWidget.setObjectName("centralWidget")

        self.tabWidget = QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(QRect(0, 0, 960, 698))
        self.data = QWidget()
        self.data.setObjectName("data")

        self.graphGroup = QGroupBox(self.data)
        self.graphGroup.setObjectName("graphGroupBox")
        self.graphGroup.setGeometry(QRect(0, 0, 625, 660))

        self.fig, self.ax = plt.subplots(figsize=(5,5), dpi = 100)
        plt.axis('off')
        plt.subplots_adjust(left=0.01, bottom=0.01, right=0.98, top=1.0, wspace=0.1, hspace=0.1)
        self.graph_plot = FigureCanvasQTAgg(self.fig)
        self.vbox = QHBoxLayout()
        self.vbox.addWidget(self.graph_plot)
        self.graphGroup.setLayout(self.vbox)

        self.graphSettingsGroup = QGroupBox(self.data)
        self.graphSettingsGroup.setObjectName("graphSettingsGroup")
        self.graphSettingsGroup.setGeometry(QRect(635, 0, 310, 660))

        self.label_topology = QLabel(self.graphSettingsGroup)
        self.label_topology.setObjectName("label_topology")
        self.label_topology.setGeometry(QRect(10, 20, 64, 16))

        self.topology_comboBox = QComboBox(self.graphSettingsGroup)
        self.topology_comboBox.setObjectName("topology_comboBox")
        self.topology_comboBox.setGeometry(QRect(80, 18, 120, 22))
        self.topology_comboBox.addItems(["Полносвязанная", "Ячеистая", "Звезда", "Кольцо", "Древовидное"])

        self.topology_Button = QPushButton(self.graphSettingsGroup)
        self.topology_Button.setObjectName("topology_Button")
        self.topology_Button.setGeometry(QRect(10, 50, 75, 24))
        self.topology_Button.clicked.connect(self.createGraphClick)

        self.label_start_node = QLabel(self.graphSettingsGroup)
        self.label_start_node.setObjectName("label_start_node")
        self.label_start_node.setGeometry(QRect(10, 84, 100, 16))

        self.start_node_lineEdit = QLineEdit(self.graphSettingsGroup)
        self.start_node_lineEdit.setObjectName("start_node_lineEdit")
        self.start_node_lineEdit.setGeometry(QRect(110, 82, 130, 22))

        self.label_end_node = QLabel(self.graphSettingsGroup)
        self.label_end_node.setObjectName("label_end_node")
        self.label_end_node.setGeometry(QRect(10, 114, 100, 16))

        self.end_node_lineEdit = QLineEdit(self.graphSettingsGroup)
        self.end_node_lineEdit.setObjectName("end_node_lineEdit")
        self.end_node_lineEdit.setGeometry(QRect(110, 112, 130, 22))

        self.label_failure_node = QLabel(self.graphSettingsGroup)
        self.label_failure_node.setObjectName("label_failure_node")
        self.label_failure_node.setGeometry(QRect(10, 144, 124, 16))

        self.failure_node_table = QTableWidget(self.graphSettingsGroup)
        self.failure_node_table.setObjectName("failure_node_table")
        self.failure_node_table.setGeometry(QRect(10, 165, 295, 160))
        self.failure_node_table.setColumnCount(2)
        self.failure_node_table.setHorizontalHeaderLabels(["Узел", "Интенсивность отказа"])
        self.failure_node_table.setColumnWidth(0, 20)
        self.failure_node_table.setColumnWidth(1, 180)
        self.failure_node_table.resizeRowsToContents()

        self.label_length_connection = QLabel(self.graphSettingsGroup)
        self.label_length_connection.setObjectName("label_length_connection")
        self.label_length_connection.setGeometry(QRect(10, 335, 130, 16))

        self.length_connection_table = QTableWidget(self.graphSettingsGroup)
        self.length_connection_table.setObjectName("length_connection_table")
        self.length_connection_table.setGeometry(QRect(10, 355, 295, 160))
        self.length_connection_table.setColumnCount(2)
        self.length_connection_table.setHorizontalHeaderLabels(["Линия", "Длина"])
        self.length_connection_table.setColumnWidth(0, 50)
        self.length_connection_table.setColumnWidth(1, 180)
        self.length_connection_table.resizeRowsToContents()

        self.label_intensity_connection = QLabel(self.graphSettingsGroup)
        self.label_intensity_connection.setObjectName("label_intensity_connection")
        self.label_intensity_connection.setGeometry(QRect(10, 525, 160, 16))

        self.intensity_connection_lineEdit = QLineEdit(self.graphSettingsGroup)
        self.intensity_connection_lineEdit.setObjectName("intensity_connection_lineEdit")
        self.intensity_connection_lineEdit.setGeometry(QRect(175, 523, 130, 22))

        self.is_recovery_checkBox = QCheckBox(self.graphSettingsGroup)
        self.is_recovery_checkBox.setObjectName("is_recovery_checkBox")
        self.is_recovery_checkBox.setGeometry(QRect(10, 555, 160, 20))

        self.simulation_Button = QPushButton(self.graphSettingsGroup)
        self.simulation_Button.setObjectName("simulation_Button")
        self.simulation_Button.setGeometry(QRect(10, 595, 80, 24))
#        self.topology_Button.clicked.connect(self.createGraphClick)

        self.tabWidget.addTab(self.data, "")
        self.result = QWidget()
        self.result.setObjectName("result")
        self.tabWidget.addTab(self.result, "")

        self.setCentralWidget(self.centralWidget)

        self.menuBar = QMenuBar()
        self.menuBar.setObjectName("menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 960, 22))
        self.setMenuBar(self.menuBar)

        self.menuGraph = QMenu()
        self.menuGraph.setObjectName("menuGraph")
        self.menuBar.addMenu(self.menuGraph)

        self.menu_add_graph = QAction()
        self.menu_add_graph.setObjectName("menu_add_graph")

        self.menu_delete_graph = QAction()
        self.menu_delete_graph.setObjectName("menu_delete_graph")
        self.menu_delete_graph.triggered.connect(self.deleteGraphClick)

        #self.menuGraph.addAction(self.menu_add_graph)
        self.menuGraph.addAction(self.menu_delete_graph)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Оценка надежности сетей", None))
        self.graphGroup.setTitle(QCoreApplication.translate("MainWindow", "Топология", None))
        self.graphSettingsGroup.setTitle(QCoreApplication.translate("MainWindow", "Настройки графа", None))
        self.label_topology.setText(QCoreApplication.translate("MainWindow", "Топология:", None))
        self.topology_Button.setText(QCoreApplication.translate("MainWindow", "Построить", None))
        self.label_start_node.setText(QCoreApplication.translate("MainWindow", "Начальный узел:", None))
        self.label_end_node.setText(QCoreApplication.translate("MainWindow", "Конечный узел:", None))
        self.label_failure_node.setText(QCoreApplication.translate("MainWindow", "Таблица отказа узлов:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data), QCoreApplication.translate("MainWindow", "Данные", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.result), QCoreApplication.translate("MainWindow", "Результат", None))
        self.menuGraph.setTitle(QCoreApplication.translate("MainWindow", "Граф", None))
        self.menu_add_graph.setText(QCoreApplication.translate("MainWindow", "Новый граф"))
        self.menu_delete_graph.setText(QCoreApplication.translate("MainWindow", "Удалить модель графа"))
        self.label_length_connection.setText(QCoreApplication.translate("MainWindow", "Таблица длины связей:"))
        self.label_intensity_connection.setText(QCoreApplication.translate("MainWindow", "Интенсивность отказа связи:"))
        self.is_recovery_checkBox.setText(QCoreApplication.translate("MainWindow", "Восстановление системы"))
        self.simulation_Button.setText(QCoreApplication.translate("MainWindow", "Симмуляция"))

    def createGraphClick(self):
        choice = self.topology_comboBox.currentText()
        self.presenter.handle_graph_create_button_clicked(choice)

    def deleteGraphClick(self):
        self.presenter.handle_graph_delete_button_clicked()

    def drawGraph(self, graph, labels):
        pos = drawing.spring_layout(graph)
        draw(graph, pos)
        draw_networkx_labels(graph, pos, labels=labels)
        self.graph_plot.draw()

    def clearGraph(self):
        self.fig.clf()
        self.graph_plot.draw()

    def output_table_nodes(self, failure_nodes):
        for index, node in enumerate(failure_nodes):
            self.failure_node_table.insertRow(index)
            self.failure_node_table.setItem(index, 0, QTableWidgetItem(node.name))