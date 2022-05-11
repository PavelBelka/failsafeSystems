import queue

class Repair:
    def __init__(self, type_queue):
        if type_queue == 'FIFO':
            self.queue = queue.Queue()
        elif type_queue == 'LIFO':
            self.queue = queue.LifoQueue()
        else:
            self.queue = queue.PriorityQueue()

    def add_task(self, task):
        self.queue.put(task)

    def get_task(self):
        if not self.queue.empty():
            return self.queue.get()

    def check_empty_queue(self):
        if self.queue.empty():
            return True
        else:
            return False

