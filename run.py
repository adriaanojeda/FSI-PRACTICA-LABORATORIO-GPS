import search
import time

def solve_and_print(problem, strategy_name, strategy_func):
    start = time.time()
    node = strategy_func(problem)
    end = time.time()
    
    elapsed_ms = (end - start) * 1000
    
    if node:
        path = [n.state for n in node.path()]
        path.reverse()
        
        return {
            'gen': problem.analisis['generados'],
            'vis': problem.analisis['visitados'],
            'cost': node.path_cost,
            'path': path, 
            'time': f"{elapsed_ms:.2f}ms"
        }
    else:
        return None

def main():
    test_cases = [
        ('1', 'A', 'B'), 
        ('2', 'O', 'E'), 
        ('3', 'G', 'Z'), 
        ('4', 'N', 'D'), 
        ('5', 'M', 'F')
    ]

    strategies = [
        ("Amplitud", search.breadth_first_graph_search),
        ("Profundidad", search.depth_first_graph_search),
        ("Ramif. y Acot.", search.branch_and_bound_graph_search),
        ("R. y A. con Sub.", search.astar_graph_search)
    ]

    print("\n" + "="*120)
    print(f"{'ID':<3} | {'ORIGEN':<8} | {'DESTINO':<9} | {'ESTRATEGIA':<18} | {'GEN':<5} | {'VIS':<5} | {'COST':<5} | {'TIEMPO':<9} | RUTA")
    print("="*120)

    for case_id, origin, dest in test_cases:
        problem = search.GPSProblem(origin, dest, search.romania)
        
        if case_id != '1': print("-" * 120)
        
        for strat_name, strat_func in strategies:
            res = solve_and_print(problem, strat_name, strat_func)
            
            if res:
                path_str = str(res['path']).replace("'", "") 
                print(f"{case_id:<3} | {origin:<8} | {dest:<9} | {strat_name:<18} | {res['gen']:<5} | {res['vis']:<5} | {res['cost']:<5} | {res['time']:<9} | {path_str}")
            else:
                print(f"{case_id:<3} | {origin:<8} | {dest:<9} | {strat_name:<18} | {'-':<5} | {'-':<5} | {'-':<5} | {'-':<9} | NO ENCONTRADO")

    print("="*120)
    
    print("\n\nDemostración Heurística No Admisible (Sobreestimación)")
    print("Objetivo: Mostrar que si h(n) > coste_real(n), A* puede no encontrar el óptimo.")
    
    class BadHeuristicProblem(search.GPSProblem):
        def h(self, node):
            if node.state == 'S': 
                return 1000 
            return super().h(node)

    bad_problem = BadHeuristicProblem('A', 'B', search.romania)
    
    node_opt = search.astar_graph_search(search.GPSProblem('A', 'B', search.romania))
    node_bad = search.astar_graph_search(bad_problem)
    
    print(f"\n1. A* Normal (Admisible): Coste {node_opt.path_cost}, Ruta {[n.state for n in node_opt.path()][::-1]}")
    print(f"2. A* Trucado (S=1000):   Coste {node_bad.path_cost}, Ruta {[n.state for n in node_bad.path()][::-1]}")
    print("Al sobreestimar S, A* lo evitó y tomó un camino peor (o diferente pero no garantizado).")

if __name__ == "__main__":
    main()