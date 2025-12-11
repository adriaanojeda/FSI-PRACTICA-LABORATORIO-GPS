from utils import *

class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal
        self.analisis = {'generados': 0, 'visitados': 0}

    def successor(self, state):
        raise NotImplementedError

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self):
        raise NotImplementedError

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node %s>" % (self.state,)

    def __lt__(self, other):
        return self.state < other.state

    def path(self):
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    def expand(self, problem):
        successors = []
        for (act, next_state) in problem.successor(self.state):
            s = Node(next_state, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next_state))
            successors.append(s)
        
        problem.analisis['generados'] += len(successors)
        return successors

def graph_search(problem, fringe):
    problem.analisis = {'generados': 0, 'visitados': 0}
    
    closed = set() 
    fringe.append(Node(problem.initial))
    problem.analisis['generados'] += 1 
    
    while fringe:
        node = fringe.pop()

        problem.analisis['visitados'] += 1
        
        if problem.goal_test(node.state):
            return node
        
        if node.state not in closed:
            closed.add(node.state)
            fringe.extend(node.expand(problem))
            
    return None

def breadth_first_graph_search(problem):
    return graph_search(problem, FIFOQueue())

def depth_first_graph_search(problem):
    return graph_search(problem, Stack())

def branch_and_bound_graph_search(problem):
    return graph_search(problem, PriorityQueue(f=lambda n: n.path_cost))

def astar_graph_search(problem):
    return graph_search(problem, PriorityQueue(f=lambda n: n.path_cost + problem.h(n)))

class Graph:
    def __init__(self, dict=None, directed=True):
        self.dict = dict or {}
        self.directed = directed
        if not directed:
            self.make_undirected()

    def make_undirected(self):
        for a in list(self.dict.keys()):
            for (b, dist) in list(self.dict[a].items()):
                self.connect1(b, a, dist)

    def connect1(self, A, B, distance):
        self.dict.setdefault(A, {})[B] = distance

    def get(self, a, b=None):
        links = self.dict.setdefault(a, {})
        if b is None: return links
        return links.get(b)

def UndirectedGraph(dict=None):
    return Graph(dict=dict, directed=False)

romania = UndirectedGraph(Dict(
    A=Dict(Z=75, S=140, T=118),
    B=Dict(U=85, P=101, G=90, F=211),
    C=Dict(D=120, R=146, P=138),
    D=Dict(M=75),
    E=Dict(H=86),
    F=Dict(S=99),
    H=Dict(U=98),
    I=Dict(V=92, N=87),
    L=Dict(T=111, M=70),
    O=Dict(Z=71, S=151),
    P=Dict(R=97),
    R=Dict(S=80),
    U=Dict(V=142)))

romania.locations = Dict(
    A=(91, 492), B=(400, 327), C=(253, 288), D=(165, 299),
    E=(562, 293), F=(305, 449), G=(375, 270), H=(534, 350),
    I=(473, 506), L=(165, 379), M=(168, 339), N=(406, 537),
    O=(131, 571), P=(320, 368), R=(233, 410), S=(207, 457),
    T=(94, 410), U=(456, 350), V=(509, 444), Z=(108, 531))

class GPSProblem(Problem):
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def successor(self, A):
        return [(B, B) for B in list(self.graph.get(A).keys())]

    def path_cost(self, cost_so_far, A, action, B):
        return cost_so_far + (self.graph.get(A, B) or infinity)

    def h(self, node):
        """Heurística: Distancia Euclídea"""
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return infinity