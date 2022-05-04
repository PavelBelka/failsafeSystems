from PyQt6.QtWidgets import QWidget, QTabWidget, QLabel, QPushButton, QMenuBar, QMenu, QGroupBox, QComboBox, \
    QMainWindow, QHBoxLayout, QLineEdit, QTableWidget, QTableWidgetItem, QCheckBox, QSpinBox, QDoubleSpinBox, \
    QRadioButton, QVBoxLayout
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
        self.settings = QWidget()
        self.settings.setObjectName("settings")

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
        self.label_intensity_connection.setGeometry(QRect(10, 525, 210, 16))

        self.intensity_connection_lineEdit = QLineEdit(self.graphSettingsGroup)
        self.intensity_connection_lineEdit.setObjectName("intensity_connection_lineEdit")
        self.intensity_connection_lineEdit.setGeometry(QRect(225, 523, 80, 22))

        self.is_recovery_checkBox = QCheckBox(self.graphSettingsGroup)
        self.is_recovery_checkBox.setObjectName("is_recovery_checkBox")
        self.is_recovery_checkBox.setGeometry(QRect(10, 555, 160, 20))

        self.simulation_Button = QPushButton(self.graphSettingsGroup)
        self.simulation_Button.setObjectName("simulation_Button")
        self.simulation_Button.setGeometry(QRect(10, 595, 80, 24))
        self.simulation_Button.clicked.connect(self.simulateClick)

        self.label_number_failing = QLabel(self.settings)
        self.label_number_failing.setObjectName("label_number_failing")
        self.label_number_failing.setGeometry(QRect(5, 10, 170, 16))

        self.number_failing_spinBox = QSpinBox(self.settings)
        self.number_failing_spinBox.setObjectName("number_failing_spinBox")
        self.number_failing_spinBox.setGeometry(QRect(185, 9, 100, 22))
        self.number_failing_spinBox.setMaximum(1000000000)
        self.number_failing_spinBox.setDisplayIntegerBase(10)

        self.label_number_repair_teams = QLabel(self.settings)
        self.label_number_repair_teams.setObjectName("label_number_repair_teams")
        self.label_number_repair_teams.setGeometry(QRect(5, 41, 175, 16))

        self.number_repair_teams_spinBox = QSpinBox(self.settings)
        self.number_repair_teams_spinBox.setObjectName("number_repair_teams_spinBox")
        self.number_repair_teams_spinBox.setGeometry(QRect(185, 40, 100, 22))

        self.label_intensity_repair = QLabel(self.settings)
        self.label_intensity_repair.setObjectName("label_intensity_repair")
        self.label_intensity_repair.setGeometry(QRect(4, 73, 179, 16))

        self.intensity_repair_spinBox = QDoubleSpinBox(self.settings)
        self.intensity_repair_spinBox.setObjectName("intensity_repair_spinBox")
        self.intensity_repair_spinBox.setGeometry(QRect(185, 72, 100, 22))
        self.intensity_repair_spinBox.setSingleStep(0.01)

        self.politicsRepairGroupBox = QGroupBox(self.settings)
        self.politicsRepairGroupBox.setObjectName("politicsRepairGroupBox")
        self.politicsRepairGroupBox.setGeometry(QRect(305, 0, 170, 115))

        self.widget = QWidget(self.politicsRepairGroupBox)
        self.widget.setObjectName("widget")
        self.widget.setGeometry(QRect(10, 19, 91, 86))

        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.politics_LIFO_radioButton = QRadioButton(self.widget)
        self.politics_LIFO_radioButton.setObjectName("politics_LIFO_radioButton")
        self.verticalLayout.addWidget(self.politics_LIFO_radioButton)

        self.politics_FIFO_radioButton = QRadioButton(self.widget)
        self.politics_FIFO_radioButton.setObjectName("politics_FIFO_radioButton")
        self.verticalLayout.addWidget(self.politics_FIFO_radioButton)

        self.politics_FAST_radioButton = QRadioButton(self.widget)
        self.politics_FAST_radioButton.setObjectName("politics_FAST_radioButton")
        self.verticalLayout.addWidget(self.politics_FAST_radioButton)

        self.politics_LONG_radioButton = QRadioButton(self.widget)
        self.politics_LONG_radioButton.setObjectName("politics_LONG_radioButton")
        self.verticalLayout.addWidget(self.politics_LONG_radioButton)

        self.save_settings_Button = QPushButton(self.settings)
        self.save_settings_Button.setObjectName("save_settings_Button")
        self.save_settings_Button.setGeometry(QRect(5, 125, 75, 24))
        self.save_settings_Button.clicked.connect(self.saveSettingsClick)

        self.tabWidget.addTab(self.data, "")
        self.tabWidget.addTab(self.settings, "")
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
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.settings), QCoreApplication.translate("MainWindow", "Доп. настройки", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.result), QCoreApplication.translate("MainWindow", "Результат", None))
        self.menuGraph.setTitle(QCoreApplication.translate("MainWindow", "Граф", None))
        self.menu_add_graph.setText(QCoreApplication.translate("MainWindow", "Новый граф"))
        self.menu_delete_graph.setText(QCoreApplication.translate("MainWindow", "Удалить модель графа"))
        self.label_length_connection.setText(QCoreApplication.translate("MainWindow", "Таблица длины связей:"))
        self.label_intensity_connection.setText(QCoreApplication.translate("MainWindow", "Удельная интенсивность отказа связи:"))
        self.is_recovery_checkBox.setText(QCoreApplication.translate("MainWindow", "Восстановление системы"))
        self.simulation_Button.setText(QCoreApplication.translate("MainWindow", "Симмуляция"))
        self.label_number_failing.setText(QCoreApplication.translate("MainWindow", "Количество отказов в системе:", None))
        self.label_number_repair_teams.setText(QCoreApplication.translate("MainWindow", "Количество ремонтных бригад:", None))
        self.label_intensity_repair.setText(QCoreApplication.translate("MainWindow", "Интенсивность восстановления:", None))
        self.politicsRepairGroupBox.setTitle(QCoreApplication.translate("MainWindow", "Политика восстановления", None))
        self.politics_LIFO_radioButton.setText(QCoreApplication.translate("MainWindow", "LIFO", None))
        self.politics_FIFO_radioButton.setText(QCoreApplication.translate("MainWindow", "FIFO", None))
        self.politics_FAST_radioButton.setText(QCoreApplication.translate("MainWindow", "FAST_FIRST", None))
        self.politics_LONG_radioButton.setText(QCoreApplication.translate("MainWindow", "LONG_FIRST", None))
        self.save_settings_Button.setText(QCoreApplication.translate("MainWindow", "Сохранить", None))

    def createGraphClick(self):
        choice = self.topology_comboBox.currentText()
        self.presenter.handle_graph_create_button_clicked(choice)

    def deleteGraphClick(self):
        self.presenter.handle_graph_delete_button_clicked()

    def saveSettingsClick(self):
        check = None
        if self.politics_LIFO_radioButton.isChecked():
            check = 'LIFO'
        elif self.politics_FIFO_radioButton.isChecked():
            check = 'FIFO'
        elif self.politics_FAST_radioButton.isChecked():
            check = 'FAST_FIRST'
        elif self.politics_LONG_radioButton.isChecked():
            check = 'LONG_FIRST'
        self.presenter.handle_save_settings_button_clicked(self.number_failing_spinBox.value(),
                                                           self.number_repair_teams_spinBox.value(),
                                                           self.intensity_repair_spinBox.value(),
                                                           check)

    def simulateClick(self):
        dict_node_table = dict()
        dict_edge_table = dict()
        for i in range(self.failure_node_table.rowCount()):
            try:
                dict_node_table[self.failure_node_table.item(i,0).text()] = self.failure_node_table.item(i, 1).text()
            except:
                dict_node_table['err'] = 'err'
        for i in range(self.length_connection_table.rowCount()):
            try:
                dict_edge_table[self.length_connection_table.item(i,0).text()] = self.length_connection_table.item(i, 1).text()
            except:
                dict_edge_table['err'] = 'err'
        self.presenter.handle_start_simulate_button_clicked(self.start_node_lineEdit.text(), self.end_node_lineEdit.text(),
                                                            dict_node_table, dict_edge_table, self.intensity_connection_lineEdit.text(),
                                                            self.is_recovery_checkBox.isChecked())

    def drawGraph(self, graph, labels):
        pos = drawing.spring_layout(graph)
        draw(graph, pos)
        draw_networkx_labels(graph, pos, labels=labels)
        self.graph_plot.draw()

    def clearGraph(self):
        self.fig.clf()
        self.graph_plot.draw()

    def clearTables(self):
        self.failure_node_table.setRowCount(0)
        self.length_connection_table.setRowCount(0)

    def output_table_nodes(self, failure_nodes):
        for index, node in enumerate(failure_nodes):
            self.failure_node_table.insertRow(index)
            self.failure_node_table.setItem(index, 0, QTableWidgetItem(node.name))

    def output_table_edges(self, edges):
        for index, edge in enumerate(edges):
            self.length_connection_table.insertRow(index)
            self.length_connection_table.setItem(index, 0, QTableWidgetItem(edge.name))

    def set_settings(self, settings):
        self.number_failing_spinBox.setValue(settings[0])
        self.number_repair_teams_spinBox.setValue(settings[1])
        self.intensity_repair_spinBox.setValue(settings[2])
        if settings[3] == 'LIFO':
            self.politics_LIFO_radioButton.setChecked(True)
        elif settings[3] == 'FIFO':
            self.politics_FIFO_radioButton.setChecked(True)
        elif settings[3] == 'FAST_FIRST':
            self.politics_FAST_radioButton.setChecked(True)
        elif settings[3] == 'LONG_FIRST':
            self.politics_LONG_radioButton.setChecked(True)