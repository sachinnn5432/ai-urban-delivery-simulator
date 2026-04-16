import math

# For the car simulator, we will treat Minimax as a strategic decision
# where the Car (MAX) wants to maximize a path value,
# and Traffic/Road Conditions (MIN) minimize it.

def minimax(node, depth, maximizing_player, grid, goal):
    """
    Simulates a strategic decision tree for path selection.
    node: current grid position
    depth: how far to look ahead
    """
    if depth == 0 or node == goal:
        # Heuristic: Negative Manhattan distance (closer is higher value)
        return - (abs(node[0] - goal[0]) + abs(node[1] - goal[1])), node

    neighbors = grid.get_neighbors(node)
    if not neighbors:
        return -float('inf'), node

    if maximizing_player:
        max_eval = -float('inf')
        best_move = neighbors[0]
        for neighbor in neighbors:
            eval_val, _ = minimax(neighbor, depth - 1, False, grid, goal)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = neighbor
        return max_eval, best_move
    else:
        # Adversarial Traffic trying to hinder movement
        min_eval = float('inf')
        best_move = neighbors[0]
        for neighbor in neighbors:
            # Min player (Traffic) chooses move that pushes car further from goal
            eval_val, _ = minimax(neighbor, depth - 1, True, grid, goal)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = neighbor
        return min_eval, best_move

def alpha_beta(node, depth, alpha, beta, maximizing_player, grid, goal):
    """
    Minimax with Alpha-Beta Pruning.
    """
    if depth == 0 or node == goal:
        return - (abs(node[0] - goal[0]) + abs(node[1] - goal[1])), node

    neighbors = grid.get_neighbors(node)
    if not neighbors:
        return -float('inf'), node

    if maximizing_player:
        max_eval = -float('inf')
        best_move = neighbors[0]
        for neighbor in neighbors:
            eval_val, _ = alpha_beta(neighbor, depth - 1, alpha, beta, False, grid, goal)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = neighbor
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break # Pruning
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = neighbors[0]
        for neighbor in neighbors:
            eval_val, _ = alpha_beta(neighbor, depth - 1, alpha, beta, True, grid, goal)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = neighbor
            beta = min(beta, eval_val)
            if beta <= alpha:
                break # Pruning
        return min_eval, best_move

def run_adversarial_sim(grid, start, goal, use_alpha_beta=False):
    """Returns a full path calculated using depth-limited adversarial search at each step."""
    path = [start]
    current = start
    explored_nodes = 0
    
    # We limit depth for real-time visualization
    MAX_DEPTH = 3 
    
    while current != goal:
        explored_nodes += 1
        if use_alpha_beta:
            _, next_node = alpha_beta(current, MAX_DEPTH, -float('inf'), float('inf'), True, grid, goal)
        else:
            _, next_node = minimax(current, MAX_DEPTH, True, grid, goal)
            
        if next_node == current: # Stuck
            break
            
        current = next_node
        path.append(current)
        yield ("visit", next_node)
        if len(path) > 100: break # Safety break
        
    return path, explored_nodes
