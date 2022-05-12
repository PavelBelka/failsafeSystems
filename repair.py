import queue

class Repair:
    def __init__(self, type_queue):
        self.type_queue = type_queue
        if self.type_queue == 'FIFO':
            self.queue = queue.Queue()
        elif self.type_queue == 'LIFO':
            self.queue = queue.LifoQueue()
        else:
            self.queue = queue.PriorityQueue()

    def add_task(self, task):
        if self.type_queue == "FAST_FIRST":
            self.queue.put((task[2], task))
        elif self.type_queue == "LONG_FIRST":
            self.queue.put((-1 * task[2], task))
        else:
            self.queue.put(task)

    def get_task(self):
        if not self.queue.empty():
            if self.type_queue == "FAST_FIRST":
                task = self.queue.get()
                return task[1]
            elif self.type_queue == "LONG_FIRST":
                task = self.queue.get()
                return task[1]
            else:
                return self.queue.get()

    def check_empty_queue(self):
        if self.queue.empty():
            return True
        else:
            return False

