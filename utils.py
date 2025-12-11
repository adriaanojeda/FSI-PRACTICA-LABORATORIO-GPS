import math
import heapq
import operator 

infinity = float('inf')

def abstract():
    raise NotImplementedError("Abstract method")

def Dict(**entries):
    return entries

def distance(a, b):
    (ax, ay) = a
    (bx, by) = b
    return math.hypot((ax - bx), (ay - by))

class Queue:
    def __init__(self):
        abstract()
    def extend(self, items):
        for item in items:
            self.append(item)

class FIFOQueue(Queue):
    def __init__(self):
        self.A = []
        self.start = 0
    def append(self, item):
        self.A.append(item)
    def __len__(self):
        return len(self.A) - self.start
    def extend(self, items):
        self.A.extend(items)
    def pop(self):
        e = self.A[self.start]
        self.start += 1
        return e

class Stack(Queue):
    def __init__(self):
        self.A = []
    def append(self, item):
        self.A.append(item)
    def __len__(self):
        return len(self.A)
    def pop(self):
        return self.A.pop()

class PriorityQueue(Queue):
    def __init__(self, f=lambda x: x):
        self.heap = []
        self.f = f

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def __len__(self):
        return len(self.heap)

    def __contains__(self, item):
        return any(item == pair[1] for pair in self.heap)

    def __getitem__(self, key):
        for _, item in self.heap:
            if item == key: return item

    def __delitem__(self, key):
        try:
            del self.heap[[item == key for _, item in self.heap].index(True)]
            heapq.heapify(self.heap)
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")