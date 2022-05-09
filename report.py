import numpy
from numpy import average, max, min

class Report:
    def __init__(self):
        self.min_time = None
        self.max_time = None
        self.average_time = None
        self.histogram_failure = None
        self.histogram_repair = None
        self.num_bars = 50

    def calculation_min_time(self, data):
        self.min_time = min(data)

    def calculation_max_time(self, data):
        self.max_time = max(data)

    def calculation_average_time(self, data):
        self.average_time = average(data)

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
        return [self.min_time, self.max_time, self.average_time]

    def get_histogram_failure(self):
        return self.histogram_failure