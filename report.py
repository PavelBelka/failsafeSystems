import numpy as np

class Report:
    def __init__(self):
        self.min_time = None
        self.max_time = None
        self.average_time_failure = None
        self.average_time_repair = None
        self.coefficient_ready = None
        self.histogram_failure = None
        self.histogram_repair = None
        self.repair_diagram = None
        self.last_diagram_timestamp = None
        self.num_bars = 100

    def calculation_min_time(self, data):
        self.min_time = np.min(data)

    def calculation_max_time(self, data):
        self.max_time = np.max(data)

    def calculation_average_time(self, data):
        self.average_time_failure = np.average(data)

    def calculation_average_time_repair(self, data):
        self.average_time_repair = np.average(data)

    def calculation_coefficient_ready(self):
        self.coefficient_ready = self.average_time_failure / (self.average_time_failure + self.average_time_repair)


    def calculate_histogram(self, data, min_data = None, max_data = None, internal = True, repair = False):
        if internal:
            minimum = np.min(data)
            maximum = np.max(data)
        else:
            minimum = min_data
            maximum = max_data
        if repair:
            self.histogram_repair = np.histogram(data, self.num_bars, (minimum, maximum), density=False)
        else:
            self.histogram_failure = np.histogram(data, self.num_bars, (minimum, maximum), density=False)

    def set_repair_diagram(self, data, timestamp):
        self.repair_diagram = data
        self.last_diagram_timestamp = timestamp

    def get_data_result(self):
        return [self.min_time, self.max_time, self.average_time_failure, self.average_time_repair, self.coefficient_ready]

    def get_histogram_failure(self):
        return self.histogram_failure

    def get_histogram_repair(self):
        return self.histogram_repair

    @staticmethod
    def calculate_graph_probability(list_data):
        common_multiply = 1.0
        for probability in list_data[1]:
            object_probability = np.subtract(1, np.exp(np.multiply(-probability, list_data[0])))
            common_multiply = np.multiply(common_multiply, object_probability)
        common_probability = np.subtract(1, common_multiply)
        return common_probability

    def output_probability(self, data):
        common_list = []
        probability_list = []
        x = np.linspace(0, self.max_time / 90, 100)
        common_list.append(x)
        for item in data:
            sum_prob = 0
            for obj in item:
                sum_prob = sum_prob + obj[1]
            probability_list.append(sum_prob)
        common_list.append(probability_list)
        result = self.calculate_graph_probability(common_list)
        return [result, x]

    def output_repair_diagram(self, nodes, edges):
        all_elements = nodes + edges
        dict_elements = {element.name: [] for element in all_elements}
        repair_elements = self.repair_diagram.copy()
        for item in all_elements:
            frame = []
            suma = 0
            for diagram in repair_elements:
                if item.name == diagram[0]:
                    if diagram[1] == 'refusal':
                        frame.append([diagram[2], 'green'])
                        suma+= diagram[2]
                    elif diagram[1] == 'restore':
                        frame.append([diagram[2], 'red'])
            if suma != 0:
                if len(frame) == 1:
                    frame.append([self.last_diagram_timestamp + 10, 'red'])
                elif frame[-1][1] == 'red':
                    frame.append([self.last_diagram_timestamp + 10, 'green'])
            if suma == 0:
                dict_elements[item.name].append([self.last_diagram_timestamp + 10, 'green'])
            else:
                dict_elements[item.name].extend(frame)
        return dict_elements
