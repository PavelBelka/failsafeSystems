import networkx, random, math

class Simulation:
    def __init__(self, graph: networkx, num_failure, num_teams, intensity_recovery, police_repair, is_repair):
        self.graph = graph
        self.num_failure = num_failure
        self.num_teams = num_teams
        self.intensity_recovery = intensity_recovery
        self.police_repair = police_repair
        self.is_repair = is_repair
        self.graph_simulate = None
        self.list_elements = None
        self.list_failure_times = []

    def get_all_elements(self, list_edges, list_nodes):
        common_list = []
        list_node = list(self.graph.nodes)
        for item in list_node:
            for node in list_nodes:
                if item == node.index:
                    common_list.append(node)
                    break
            for edge in list_edges:
                if item == edge.tuple_node[0]:
                    common_list.append(edge)
        return common_list

    def restore_state(self):
        for item in self.list_elements:
            item.destroyed = False

    def start_simulation(self, start_node, end_node, list_edges, list_nodes):
        is_path = networkx.shortest_paths.has_path(self.graph, start_node, end_node)
        self.list_elements = self.get_all_elements(list_edges, list_nodes)
        self.restore_state()
        if is_path:
            for i in range(self.num_failure):
                self.graph_simulate = self.graph
                self.restore_state()
                state = self.system_iteration(start_node, end_node)
                self.list_failure_times.append(state)

    def system_iteration(self, start_node, end_node):
        timestamp = 0.0
        list_task = []

        #Первый отказ
        first_failure = self.generate_failure(timestamp)

        #Заносим хранилище задач
        list_task.append(first_failure)

        #Цикл пока есть путь
        while networkx.shortest_paths.has_path(self.graph, start_node, end_node):
            min_element = list_task[0]

            #FIFO
            for item in list_task:
                if item[0] < min_element[0]:
                    min_element = item
            list_task.remove(min_element)
            timestamp = min_element[0]
            if min_element[3] == 'refusal':
                min_element[1].destroyed = True
                failure = self.generate_failure(timestamp)
                list_task.append(failure)

                #Чиним?
                if self.is_repair:
                    pass
        return [timestamp]

    def generate_failure(self, timestamp):
        total = 0.0
        sums = 0
        element_fail = None
        for element in self.list_elements:
            if not element.destroyed:
                total = total + element.intensity
        random_value = random.random()
        rand = random_value * total
        for element in self.list_elements:
            if not element.destroyed:
                sums = sums + element.intensity
                if sums > rand:
                    element_fail = element
                    break
        if element_fail is None:
            return  None
        time_fail = -1 * math.log(random_value) / element_fail.intensity
        timestamp = timestamp + time_fail
        return [timestamp, element_fail, 'refusal']