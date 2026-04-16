from ai.search import a_star

def optimize_delivery(grid, start, targets):
    """
    Optimizes the path to visit all target points.
    Uses A* for point-to-point and Nearest Neighbor for sequence.
    """
    current_pos = start
    remaining_targets = list(targets)
    full_path = [start]
    total_nodes_explored = 0
    
    while remaining_targets:
        # Find the geometrically nearest target (heuristic-wise)
        # to speed up the decision, then use A* for actual path
        nearest_target = min(remaining_targets, 
                             key=lambda t: abs(t[0] - current_pos[0]) + abs(t[1] - current_pos[1]))
        
        # Generator for A*
        path_gen = a_star(grid, current_pos, nearest_target)
        
        # Consume the generator (we might want to visualize this though)
        path = None
        for step in path_gen:
            if isinstance(step, list): # The final return from generator-ified a_star
                path, nodes = step
                break
            # Logic to handle if a_star is used as a generator
            # We'll refine a_star to optionally return final result directly or just extract it
        
        # WAIT: Let's re-run a_star as a function here or handle the generator
        # I'll re-implement a simple non-generator version or just pull values
        
        # Let's use a dedicated path finder for TSP
        sub_path, nodes = find_shortest_path(grid, current_pos, nearest_target)
        if sub_path:
            full_path.extend(sub_path[1:]) # Skip the first node as it's the current_pos
            total_nodes_explored += nodes
            current_pos = nearest_target
            remaining_targets.remove(nearest_target)
        else:
            # Cannot reach target
            break
            
    return full_path, total_nodes_explored

def find_shortest_path(grid, start, goal):
    """Utility for point to point search without yielding."""
    from ai.search import a_star
    gen = a_star(grid, start, goal)
    while True:
        try:
            next(gen)
        except StopIteration as e:
            return e.value
