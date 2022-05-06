from numpy import average, max, min

class Report:
    def __init__(self):
        self.min_time = None
        self.max_time = None
        self.average_time = None

    def calculation_min_time(self, data):
        self.min_time = min(data)

    def calculation_max_time(self, data):
        self.max_time = max(data)

    def calculation_average_time(self, data):
        self.average_time = average(data)

    def get_data(self):
        return [self.min_time, self.max_time, self.average_time]