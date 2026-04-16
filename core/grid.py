from vpython import box, vector, color, scene, canvas, random, cylinder, sphere, local_light, textures
from utils.constants import (GRID_SIZE, CELL_SIZE, COLOR_ROAD, COLOR_OBSTACLE, 
                             COLOR_START, COLOR_DESTINATION, COLOR_MARKING, 
                             COLOR_LAMP_POST, COLOR_LAMP_WARM, COLOR_WINDOW)

class Grid:
    def __init__(self):
        self.size = GRID_SIZE
        self.cells = {}
        self.obstacles = set()
        self.decorations = []
        self.start_pos = (0, 0)
        self.dest_pos = (GRID_SIZE - 1, GRID_SIZE - 1)
        self.multi_targets = []
        
        self._create_infinity_ground()
        self._create_grid()
        self._create_cityscape()

    def _create_infinity_ground(self):
        # Huge textured industrial plane for depth
        box(pos=vector(0, -0.4, 0), size=vector(800, 0.1, 800), 
            color=vector(0.1, 0.1, 0.13), texture=textures.rough)

    def _create_grid(self):
        offset = (self.size * CELL_SIZE) / 2 - (CELL_SIZE / 2)
        
        for r in range(self.size):
            for c in range(self.size):
                x = c * CELL_SIZE - offset
                z = r * CELL_SIZE - offset
                
                # Asphalt road with detailed texture & shininess
                b = box(pos=vector(x, -0.1, z), 
                        size=vector(CELL_SIZE, 0.2, CELL_SIZE),
                        color=COLOR_ROAD, shininess=0.15, texture=textures.rough)
                
                # Lane Markings (Sophisticated dashed lines)
                if c < self.size - 1:
                    box(pos=vector(x + CELL_SIZE/2, -0.05, z), 
                        size=vector(0.04, 0.11, 0.35), color=COLOR_MARKING)
                if r < self.size - 1:
                    box(pos=vector(x, -0.05, z + CELL_SIZE/2), 
                        size=vector(0.35, 0.11, 0.04), color=COLOR_MARKING)
                
                b.grid_pos = (r, c)
                self.cells[(r, c)] = b
                
        self.set_start(*self.start_pos)
        self.set_destination(*self.dest_pos)

    def _create_cityscape(self):
        offset = (self.size * CELL_SIZE) / 2 - (CELL_SIZE / 2)
        
        # Professional Intersectional Street Lamps
        for pair in [(1,1), (1, GRID_SIZE-2), (GRID_SIZE-2, 1), (GRID_SIZE-2, GRID_SIZE-2)]:
            r, c = pair
            lx = c * CELL_SIZE - offset
            lz = r * CELL_SIZE - offset
            # Lamp Post
            cylinder(pos=vector(lx, -0.1, lz), axis=vector(0, 3.5, 0), radius=0.06, color=COLOR_LAMP_POST)
            # Arm
            cylinder(pos=vector(lx, 3.4, lz), axis=vector(0.4, 0, 0), radius=0.03, color=COLOR_LAMP_POST)
            # Glowing Head
            sphere(pos=vector(lx+0.4, 3.4, lz), radius=0.12, color=COLOR_LAMP_WARM, emissive=True)
            # High-fidelity Local Light
            local_light(pos=vector(lx+0.4, 3.2, lz), color=COLOR_LAMP_WARM)

        # High-rise Skyscraper Generator with Window Patterns
        for r in range(-20, self.size + 20, 4):
            for c in range(-20, self.size + 20, 4):
                if not (-4 <= r < self.size + 4 and -4 <= c < self.size + 4):
                    bx = c * CELL_SIZE - offset
                    bz = r * CELL_SIZE - offset
                    h = random() * 10 + 5
                    # Main Building
                    main_b = box(pos=vector(bx, h/2 - 0.2, bz),
                                size=vector(CELL_SIZE*2.5, h, CELL_SIZE*2.5),
                                color=vector(0.18, 0.18, 0.22), texture=textures.stucco)
                    # Window Lights
                    for wh in range(2, int(h), 2):
                        if random() > 0.4:
                            box(pos=vector(bx, wh, bz + CELL_SIZE*1.26), size=vector(0.4, 0.3, 0.05), color=COLOR_WINDOW, emissive=True)
                            box(pos=vector(bx + CELL_SIZE*1.26, wh, bz), size=vector(0.05, 0.3, 0.4), color=COLOR_WINDOW, emissive=True)

    def set_start(self, r, c):
        self.cells[self.start_pos].color = COLOR_ROAD
        self.cells[self.start_pos].emissive = False
        self.start_pos = (r, c)
        self.cells[r, c].color = COLOR_START
        self.cells[r, c].emissive = True

    def set_destination(self, r, c):
        self.cells[self.dest_pos].color = COLOR_ROAD
        self.cells[self.dest_pos].emissive = False
        self.dest_pos = (r, c)
        self.cells[r, c].color = COLOR_DESTINATION
        self.cells[r, c].emissive = True

    def toggle_obstacle(self, r, c):
        if (r, c) == self.start_pos or (r, c) == self.dest_pos: return
        if (r, c) in self.obstacles:
            self.obstacles.remove((r, c))
            self.cells[r, c].color = COLOR_ROAD
        else:
            self.obstacles.add((r, c))
            self.cells[r, c].color = COLOR_OBSTACLE

    def get_neighbors(self, pos):
        r, c = pos
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                if (nr, nc) not in self.obstacles:
                    neighbors.append((nr, nc))
        return neighbors

    def reset_viz(self):
        for pos, b in self.cells.items():
            b.emissive = False
            if pos == self.start_pos:
                b.color = COLOR_START
                b.emissive = True
            elif pos == self.dest_pos:
                b.color = COLOR_DESTINATION
                b.emissive = True
            elif pos in self.obstacles:
                b.color = COLOR_OBSTACLE
            elif pos in self.multi_targets:
                b.color = COLOR_DESTINATION
                b.emissive = True
            else:
                b.color = COLOR_ROAD

    def highlight_visited(self, pos):
        if pos != self.start_pos and pos != self.dest_pos:
            self.cells[pos].color = vector(0.2, 0.2, 0.25)

    def highlight_path(self, path):
        from utils.constants import COLOR_PATH
        for pos in path:
            if pos != self.start_pos and pos != self.dest_pos:
                self.cells[pos].color = COLOR_PATH
                self.cells[pos].emissive = False

    def get_3d_pos(self, pos):
        return self.cells[pos].pos
