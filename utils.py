import math
import heapq
import operator 

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
    def __init__(self, order='min', f=lambda x: x):
        self.heap = []
        if order == 'min':
            self.f = f
        elif order == 'max':
            self.f = lambda x: -f(x)
        else:
            raise ValueError("order must be 'min' or 'max'")

    def append(self, item):
        heapq.heappush(self.heap, (self.f(item), item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def __len__(self):
        return len(self.heap)