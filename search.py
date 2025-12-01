from utils import * 

# ______________________________________________________________________________
# CÓDIGO BASE (Respetando interfaces originales) [cite: 8]

class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def successor(self, state):
        abstract()

    def goal_test(self, state):
        return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self):
        abstract()

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
    
    # Añadido: Necesario para que PriorityQueue compare nodos en caso de empate de costes
    def __lt__(self, other):
        return self.state < other.state

    def path(self):
        x, result = self, [self]
        while x.parent:
            result.append(x.parent)
            x = x.parent
        return result

    def expand(self, problem):
        return [Node(next_state, self, act,
                     problem.path_cost(self.path_cost, self.state, act, next_state))
                for (act, next_state) in problem.successor(self.state)]

# ______________________________________________________________________________
# MODIFICACIÓN: Búsqueda instrumentada (Parte 3) 

def graph_search_instrumented(problem, fringe):
    """
    Versión modificada de graph_search que cuenta nodos.
    Retorna: (NodeSolucion, NodosGenerados, NodosVisitados)
    """
    closed = set() # Usamos set en vez de dict para eficiencia, compatible con lógica original
    
    # Contadores 
    generated_nodes = 0
    visited_nodes = 0
    
    initial_node = Node(problem.initial)
    fringe.append(initial_node)
    generated_nodes += 1 # [cite: 24] Nodos creados
    
    while len(fringe) > 0:
        node = fringe.pop()
        visited_nodes += 1 # [cite: 26] Nodos interrogados (sacados de la frontera)
        
        if problem.goal_test(node.state):
            return node, generated_nodes, visited_nodes
        
        if node.state not in closed:
            closed.add(node.state)
            successors = node.expand(problem)
            fringe.extend(successors)
            generated_nodes += len(successors) # Sumamos los generados al expandir
            
    return None, generated_nodes, visited_nodes

# Wrapper original para NO romper compatibilidad [cite: 8]
def graph_search(problem, fringe):
    result, _, _ = graph_search_instrumented(problem, fringe)
    return result

# ______________________________________________________________________________
# ESTRATEGIAS DE BÚSQUEDA

def breadth_first_graph_search(problem):
    return graph_search(problem, FIFOQueue())

def depth_first_graph_search(problem):
    return graph_search(problem, Stack())

# Parte 1: Ramificación y Acotación 
def branch_and_bound_graph_search(problem):
    # Ordena por coste de camino (g)
    return graph_search(problem, PriorityQueue(order='min', f=lambda n: n.path_cost))

# Parte 2: A* (Subestimación) [cite: 16]
def astar_graph_search(problem):
    # Ordena por f(n) = g(n) + h(n)
    return graph_search(problem, PriorityQueue(order='min', f=lambda n: n.path_cost + problem.h(n)))

# Funciones "Helper" para obtener las métricas en run.py sin romper las funciones originales
def run_search_with_metrics(problem, algorithm_name):
    fringe = None
    if algorithm_name == 'bfs': fringe = FIFOQueue()
    elif algorithm_name == 'dfs': fringe = Stack()
    elif algorithm_name == 'bab': fringe = PriorityQueue(order='min', f=lambda n: n.path_cost)
    elif algorithm_name == 'astar': fringe = PriorityQueue(order='min', f=lambda n: n.path_cost + problem.h(n))
    
    return graph_search_instrumented(problem, fringe)

# ______________________________________________________________________________
# DEFINICIÓN DE GRAFOS (Copiado del base para mantener autonomía)

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

# Mapa de Rumanía (Base code data)
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
    U=Dict(V=142),
    Z=Dict(O=71))) # Asegurado Z

romania.locations = Dict(
    A=(91, 492), B=(400, 327), C=(253, 288), D=(165, 299),
    E=(562, 293), F=(305, 449), G=(375, 270), H=(534, 350),
    I=(473, 506), L=(165, 379), M=(168, 339), N=(406, 537),
    O=(131, 571), P=(320, 368), R=(233, 410), S=(207, 457),
    T=(94, 410), U=(456, 350), V=(509, 444), Z=(108, 531))

australia = UndirectedGraph(Dict(
    T=Dict(),
    SA=Dict(WA=1, NT=1, Q=1, NSW=1, V=1),
    NT=Dict(WA=1, Q=1),
    NSW=Dict(Q=1, V=1)))

australia.locations = Dict(
WA=(120, 24), NT=(135, 20), SA=(135, 30),
Q=(145, 20), NSW=(145, 32), T=(145, 42), V=(145, 37))

class GPSProblem(Problem):
    def __init__(self, initial, goal, graph):
        Problem.__init__(self, initial, goal)
        self.graph = graph

    def successor(self, A):
        return [(B, B) for B in list(self.graph.get(A).keys())]

    def path_cost(self, cost_so_far, A, action, B):
        # path_cost soportado en código base 
        return cost_so_far + (self.graph.get(A, B) or float('inf'))

    def h(self, node):
        # Heurística distancia euclídea 
        locs = getattr(self.graph, 'locations', None)
        if locs:
            return int(distance(locs[node.state], locs[self.goal]))
        else:
            return float('inf')