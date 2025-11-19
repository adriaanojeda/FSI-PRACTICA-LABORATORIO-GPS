# Search methods

import search

# Función auxiliar para imprimir resultados
def print_results(problem, result_node, strategy_name, origen, destino):
    print(f"\n--- {strategy_name} ({origen} -> {destino}) ---")
    if result_node:
        path_list = [n.state for n in result_node.path()]
        # La función path() devuelve del nodo actual a la raíz, por eso se invierte
        path_str = ' -> '.join(reversed(path_list)) 
        cost = result_node.path_cost
        
        # Datos para la tabla comparativa (Parte 3)
        print(f"Ruta Solución: {path_str}")
        print(f"Coste Total: {cost}")
        print(f"Nodos Generados: {problem.nodes_generated}")
        print(f"Nodos Visitados: {problem.nodes_visited}")
    else:
        print("No se encontró solución.")

# Definición de los 5 problemas de la tabla: (Origen, Destino)
PROBLEMS = [
    ('A', 'B'), # Arad -> Bucharest
    ('O', 'E'), # Oradea -> Eforie
    ('G', 'Z'), # Giurgiu -> Zerind
    ('N', 'D'), # Neamt -> Dobreta
    ('M', 'F')  # Mehadia -> Fagaras
]

STRATEGIES = {
    "Búsqueda en Anchura (BFS)": search.breadth_first_graph_search,
    "Búsqueda en Profundidad (DFS)": search.depth_first_graph_search,
    "Ramificación y Acotación (UCS)": search.uniform_cost_search,
    "Ramificación y Acotación con Subestimación (A*)": search.astar_search
}

# Ejecutar todos los problemas con todas las estrategias
for origen, destino in PROBLEMS:
    print(f"\n{'='*50}")
    print(f"EJECUTANDO: {origen} -> {destino}")
    print(f"{'='*50}")
    
    for strategy_name, search_func in STRATEGIES.items():
        # Crea una nueva instancia del problema para resetear los contadores
        problem_instance = search.GPSProblem(origen, destino, search.romania)
        
        # Ejecuta la búsqueda
        result_node = search_func(problem_instance)
        
        # Imprime los resultados
        print_results(problem_instance, result_node, strategy_name, origen, destino)