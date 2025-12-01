import search
import time

def main():
    # Definimos el problema: Arad -> Bucharest
    ab = search.GPSProblem('A', 'B', search.romania)
    
    # Lista de algoritmos a ejecutar
    strategies = [
        ("Anchura (BFS)", 'bfs'),
        ("Profundidad (DFS)", 'dfs'),
        ("Ramif. y Acot. (B&B)", 'bab'), # 
        ("A* (Heurística)", 'astar')    # [cite: 16]
    ]

    print("\n--- RESULTADOS PRÁCTICA 1 (FSI) ---")
    # Cabecera de la tabla 
    print(f"{'ESTRATEGIA':<25} | {'GEN':<6} | {'VIS':<6} | {'COST':<6} | RUTA")
    print("-" * 90)

    for name, code in strategies:
        start_time = time.time()
        
        # Ejecutamos usando la versión instrumentada
        node, gen, vis = search.run_search_with_metrics(ab, code)
        
        elapsed = time.time() - start_time
        
        if node:
            # Reconstruir camino para imprimir (Invertir porque .path() va de fin a inicio)
            path_objs = node.path()
            path_names = [n.state for n in reversed(path_objs)]
            cost = node.path_cost
            
            # Imprimir fila de la tabla
            print(f"{name:<25} | {gen:<6} | {vis:<6} | {cost:<6} | {path_names}")
        else:
            print(f"{name:<25} | -      | -      | -      | No encontrada")

if __name__ == "__main__":
    main()