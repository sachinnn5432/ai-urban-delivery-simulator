import heapq
from collections import deque
import time

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def bfs(grid, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    explored_nodes = 0
    
    while queue:
        current, path = queue.popleft()
        explored_nodes += 1
        
        if current == goal:
            return path, explored_nodes
            
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
                # Use a specific yield format for visualization
                yield ("visit", neighbor)
                
    return None, explored_nodes

def dfs(grid, start, goal):
    stack = [(start, [start])]
    visited = {start}
    explored_nodes = 0
    
    while stack:
        current, path = stack.pop()
        explored_nodes += 1
        
        if current == goal:
            return path, explored_nodes
            
        for neighbor in grid.get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))
                yield ("visit", neighbor)
                
    return None, explored_nodes

def a_star(grid, start, goal):
    pq = [(0, start, [start])]
    g_score = {start: 0}
    explored_nodes = 0
    
    while pq:
        f, current, path = heapq.heappop(pq)
        explored_nodes += 1
        
        if current == goal:
            return path, explored_nodes
            
        for neighbor in grid.get_neighbors(current):
            new_g = g_score[current] + 1
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                f_score = new_g + manhattan_distance(neighbor, goal)
                heapq.heappush(pq, (f_score, neighbor, path + [neighbor]))
                yield ("visit", neighbor)
                
    return None, explored_nodes

def hill_climbing(grid, start, goal):
    current = start
    path = [start]
    explored_nodes = 0
    
    while current != goal:
        explored_nodes += 1
        neighbors = grid.get_neighbors(current)
        if not neighbors:
            break
            
        next_node = min(neighbors, key=lambda n: manhattan_distance(n, goal))
        
        if manhattan_distance(next_node, goal) >= manhattan_distance(current, goal):
            break
            
        current = next_node
        path.append(current)
        yield ("visit", current)
        
    return (path if current == goal else None), explored_nodes
