import numpy
import numpy as np
from numpy import average, max, min

class Report:
    def __init__(self):
        self.min_time = None
        self.max_time = None
        self.average_time_failure = None
        self.average_time_repair = None
        self.coefficient_ready = None
        self.histogram_failure = None
        self.histogram_repair = None
        self.num_bars = 100

    def calculation_min_time(self, data):
        self.min_time = min(data)

    def calculation_max_time(self, data):
        self.max_time = max(data)

    def calculation_average_time(self, data):
        self.average_time_failure = average(data)

    def calculation_average_time_repair(self, data):
        self.average_time_repair = average(data)

    def calculation_coefficient_ready(self):
        self.coefficient_ready = self.average_time_failure / (self.average_time_failure + self.average_time_repair)

    def calculate_histogram(self, data, min_data = None, max_data = None, internal = True, repair = False):
        if internal:
            minimum = min(data)
            maximum = max(data)
        else:
            minimum = min_data
            maximum = max_data
        if repair:
            self.histogram_repair = numpy.histogram(data, self.num_bars, (minimum, maximum), density=False)
        else:
            self.histogram_failure = numpy.histogram(data, self.num_bars, (minimum, maximum), density=False)

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