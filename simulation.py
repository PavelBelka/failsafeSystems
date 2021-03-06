import networkx, random, math
from graph import Node, Edge
from networkx import exception

from repair import Repair


class Simulation:
    def __init__(self, graph: networkx, num_failure, num_teams, intensity_recovery, police_repair, is_repair, report):
        self.graph = graph
        self.num_failure = num_failure
        self.num_teams = num_teams
        self.intensity_recovery = intensity_recovery
        self.police_repair = police_repair
        self.is_repair = is_repair
        self.report = report
        self.graph_simulate = None
        self.list_elements = None
        self.list_failure_times = []
        self.list_repair_times = []

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
                self.graph_simulate = self.graph.copy()
                self.restore_state()
                if i == 0 and self.is_repair:
                    state = self.system_iteration(start_node, end_node, True)
                    self.report.set_repair_diagram(state[2], state[0])
                else:
                    state = self.system_iteration(start_node, end_node, False)
                self.list_failure_times.append(state[0])
                if self.is_repair:
                    self.list_repair_times.extend(state[1])
            self.report.calculation_min_time(self.list_failure_times)
            self.report.calculation_max_time(self.list_failure_times)
            self.report.calculation_average_time(self.list_failure_times)
            if self.is_repair:
                self.report.calculation_average_time_repair(self.list_repair_times)
                self.report.calculation_coefficient_ready()
                self.report.calculate_histogram(self.list_repair_times, repair=True)
            self.report.calculate_histogram(self.list_failure_times)
            self.list_failure_times = None
            self.list_repair_times = None

    def system_iteration(self, start_node, end_node, is_diagram):
        timestamp = 0.0
        list_task = []
        list_repair_time = []
        if is_diagram:
            list_diagram_failure = []
        repair_tasks = Repair(self.police_repair)
        recovery_team = self.num_teams

        #???????????? ??????????
        first_failure = self.generate_failure(timestamp)

        #?????????????? ?????????????????? ??????????
        list_task.append(first_failure)

        #???????? ???????? ???????? ????????
        is_path = True
        while is_path:
            try:
                is_path = networkx.shortest_paths.has_path(self.graph_simulate, start_node, end_node)
                if not is_path:
                    break
            except (exception.NodeNotFound, exception.NetworkXNoPath):
                break
            min_element = list_task[0]

            #FIFO
            for item in list_task:
                if item[0] < min_element[0]:
                    min_element = item
            list_task.remove(min_element)
            timestamp = min_element[0]
            if min_element[2] == 'refusal':
                min_element[1].destroyed = True
                failure = self.generate_failure(timestamp)
                if isinstance(min_element[1], Node):
                    self.graph_simulate.remove_node(min_element[1].index)
                elif isinstance(min_element[1], Edge):
                    try:
                        self.graph_simulate.remove_edge(min_element[1].tuple_node[0], min_element[1].tuple_node[1])
                    except exception.NetworkXError:
                        pass
                list_task.append(failure)
                if is_diagram:
                    list_diagram_failure.append([min_element[1].name, min_element[2], timestamp])

                #???????????
                if self.is_repair:
                    repair_tasks.add_task([min_element[1],
                                           min_element[0],
                                           -1 * math.log(random.random()) / (self.intensity_recovery * 1e-2)])
            elif min_element[2] == 'restore':
                min_element[1].destroyed = False
                recovery_team += 1
                self.restore_graph(min_element[1])
                if is_diagram:
                    list_diagram_failure.append([min_element[1].name, min_element[2], timestamp])

            #?????????????? ????????????????
            while recovery_team > 0 and not repair_tasks.check_empty_queue() and self.is_repair:
                task = repair_tasks.get_task()
                list_task.append([task[2] + timestamp, task[0], 'restore'])
                recovery_team -= 1
                list_repair_time.append(task[2])
        if is_diagram:
            return [timestamp, list_repair_time, list_diagram_failure]
        else:
            return [timestamp, list_repair_time]

    def restore_graph(self, element):
        if isinstance(element, Node):
            self.graph_simulate.add_node(element.index)
            for item in self.list_elements:
                if isinstance(item, Edge):
                    if item.tuple_node[0] == element.index or item.tuple_node[1] == element.index:
                        self.graph_simulate.add_edge(item.tuple_node[0], item.tuple_node[1])
        elif isinstance(element, Edge):
            try:
                self.graph_simulate.add_edge(element.tuple_node[0], element.tuple_node[1])
            except exception.NetworkXError:
                pass

    def generate_failure(self, timestamp):
        total = 0.0
        sums = 0
        element_fail = None
        for element in self.list_elements:
            if not element.destroyed:
                total = total + element.intensity
        for element in self.list_elements:
            if not element.destroyed:
                element.conditional_intensity = element.intensity / total
        random_value = random.random()
        for element in self.list_elements:
            if not element.destroyed:
                sums = sums + element.conditional_intensity
                if sums > random_value:
                    element_fail = element
                    break
        if element_fail is None:
            return  None
        time_fail = -1 / element_fail.intensity * math.log(random_value)
        timestamp = timestamp + time_fail
        return [timestamp, element_fail, 'refusal']
