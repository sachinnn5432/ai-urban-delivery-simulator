import sys
import os
from ai.search import a_star, bfs, dfs
from ai.adversarial import minimax
from utils.constants import GRID_SIZE

class MockGrid:
    def __init__(self, size=5):
        self.size = size
        self.obstacles = set()
    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                neighbors.append((nr, nc))
        return neighbors

grid = MockGrid()
path, _ = next(a_star(grid, (0,0), (1,1)), (None, 0))
# Special check for generator
gen = a_star(grid, (0,0), (4,4))
while True:
    try:
        next(gen)
    except StopIteration as e:
        path, explored = e.value
        break
print(f"Logic Check: A* Path found with length {len(path)}")
print("SUCCESS")
