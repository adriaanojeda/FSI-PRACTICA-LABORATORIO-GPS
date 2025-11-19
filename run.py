# Search methods

import search

# Función auxiliar para imprimir resultados
def print_results(problem, result_node, strategy_name):
    print(f"\n--- {strategy_name} ---")
    if result_node:
        path_list = [n.state for n in result_node.path()]
        # La función path() devuelve del nodo actual a la raíz, por eso se invierte
        path_str = ' -> '.join(reversed(path_list)) 
        cost = result_node.path_cost
        
        # Datos para la tabla comparativa (Parte 3) [cite: 29]
        print(f"Ruta Solución: {path_str} [cite: 32]")
        print(f"Coste Total: {cost} [cite: 33]")
        print(f"Nodos Generados: {problem.nodes_generated} [cite: 30]")
        print(f"Nodos Visitados: {problem.nodes_visited} [cite: 31]")
    else:
        print("No se encontró solución.")

# Definir el problema: Buscar un camino de Arad ('A') a Bucarest ('B')
# Se crean nuevas instancias para resetear los contadores de nodos
# La distancia de A a B por el camino óptimo es 418.

# Búsqueda en Anchura (BFS)
ab_bfs = search.GPSProblem('A', 'B', search.romania)
result_bfs = search.breadth_first_graph_search(ab_bfs)
print_results(ab_bfs, result_bfs, "Búsqueda en Anchura (BFS)")

# Búsqueda en Profundidad (DFS)
ab_dfs = search.GPSProblem('A', 'B', search.romania)
result_dfs = search.depth_first_graph_search(ab_dfs)
print_results(ab_dfs, result_dfs, "Búsqueda en Profundidad (DFS)")

# Ramificación y Acotación (Uniform Cost Search / UCS) (Parte 1)
ab_ucs = search.GPSProblem('A', 'B', search.romania)
result_ucs = search.uniform_cost_search(ab_ucs)
print_results(ab_ucs, result_ucs, "Ramificación y Acotación (UCS)")

# Ramificación y Acotación con Subestimación (A* Search) (Parte 2)
ab_astar = search.GPSProblem('A', 'B', search.romania)
result_astar = search.astar_search(ab_astar)
print_results(ab_astar, result_astar, "Ramificación y Acotación con Subestimación (A*)")


# Resultados originales del código base para referencia:
# [<Node B>, <Node P>, <Node R>, <Node S>, <Node A>] : 101 + 97 + 80 + 140 = 418
# [<Node B>, <Node F>, <Node S>, <Node A>] : 211 + 99 + 140 = 450