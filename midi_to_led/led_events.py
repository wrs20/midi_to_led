from queue import PriorityQueue
from threading import Thread
import functools
import time


@functools.total_ordering
class Event:
    def __init__(self, time, func, args):
        self.time = time
        self.func = func
        self.args = args
    def __call__(self):
        self.func(*self.args)
    def __lt__(self, other):
        return self.time < other.time
    def __eq__(self, other):
        return self.time == other.time


class EventQueue:
    def __init__(self):
        self.queue = PriorityQueue()
        self.thread = Thread(target=self._process_queue)
        self.running = True

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def put(self, event):
        self.queue.put(event)

    def _process_queue(self):
        while self.running:
            if self.queue.empty():
                continue
            else:
                event = self.queue.get()

                # someone is going to get upset at this
                while time.time() < event.time:
                    pass

                event()

        self.thread = Thread(target=self._process_queue)




