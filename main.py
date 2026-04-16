from vpython import canvas, label, vector, color, rate, scene, box, distant_light, local_light, sphere
import time

from utils.constants import (SCENE_WIDTH, SCENE_HEIGHT, ANIMATION_RATE, COLOR_START, 
                             COLOR_DESTINATION, COLOR_CURSOR, COLOR_SKY, GRID_SIZE, CELL_SIZE)
from core.grid import Grid
from core.car import Car
from ai.search import bfs, dfs, a_star, hill_climbing
from ai.adversarial import run_adversarial_sim
from ai.delivery import optimize_delivery

class SimulationApp:
    def __init__(self):
        # Create Pro Canvas with Urban Atmosphere
        self.scene = canvas(title="<b>AI URBAN SIMULATOR: PRO VERSION</b>", 
                           width=SCENE_WIDTH, height=SCENE_HEIGHT, 
                           background=COLOR_SKY,
                           center=vector(0, 0, 0),
                           forward=vector(-1, -0.6, -1), # Lower cinematic angle
                           autoscale=False)
        
        # Environmental Depth (Fog)
        self.scene.fog_color = COLOR_SKY
        self.scene.fog_depth = 80
        
        # Moonlight & Ambient Control
        self.scene.lights = [] 
        distant_light(direction=vector(0.5, -1, 0.5), color=vector(0.5, 0.5, 0.6)) 
        self.scene.ambient = vector(0.1, 0.1, 0.1) # Dark night mood
        
        # Grid and Pro Car
        self.grid = Grid()
        self.car = Car(self.grid.get_3d_pos(self.grid.start_pos))
        
        # Keyboard Selector (Sleeker design)
        self.cursor_pos = [0, 0]
        self.cursor_obj = box(pos=self.grid.get_3d_pos((0,0)) + vector(0, 0.3, 0),
                             size=vector(CELL_SIZE * 1.05, 0.05, CELL_SIZE * 1.05),
                             color=color.cyan, opacity=0.6, emissive=True)
        
        # Multi-Panel Pro HUD
        self.hud_main = label(pixel_pos=True, pos=vector(40, 740, 0), 
                             text="<b>INDUSTRIAL AI HUD</b>\n[Arrows] Move | [Space] Road Patch\n[A] A-Star | [B] BFS | [D] DFS\n[T] Multi-Delivery Strategy", 
                             height=14, border=12, font='monospace', box=True, 
                             background=vector(0.01, 0.01, 0.05), opacity=0.8, align='left',
                             color=vector(0.4, 0.9, 1.0))
        
        self.hud_stats = label(pixel_pos=True, pos=vector(SCENE_WIDTH - 40, 740, 0), 
                              text="<b>SYSTEM METRICS</b>\nStatus: STANDBY\nEfficiency: 0%\nNodes: 0", 
                              height=14, border=12, font='monospace', box=True, 
                              background=vector(0.01, 0.01, 0.05), opacity=0.8, align='right',
                              color=vector(1.0, 0.9, 0.4))
        
        self.running = False
        self.scene.bind('keydown', self.on_key_down)

    def update_cursor_viz(self):
        target_pos = self.grid.get_3d_pos(tuple(self.cursor_pos))
        self.cursor_obj.pos = target_pos + vector(0, 0.3, 0)

    def on_key_down(self, evt):
        if self.running: return
        k = evt.key
        
        # Controller Mapping
        if k == 'up':
            if self.cursor_pos[0] < GRID_SIZE - 1: self.cursor_pos[0] += 1
            self.update_cursor_viz()
        elif k == 'down':
            if self.cursor_pos[0] > 0: self.cursor_pos[0] -= 1
            self.update_cursor_viz()
        elif k == 'right':
            if self.cursor_pos[1] < GRID_SIZE - 1: self.cursor_pos[1] += 1
            self.update_cursor_viz()
        elif k == 'left':
            if self.cursor_pos[1] > 0: self.cursor_pos[1] -= 1
            self.update_cursor_viz()
        elif k == ' ':
            self.grid.toggle_obstacle(*tuple(self.cursor_pos))
            
        # Logic Triggers
        elif k == 'b': self.run_algo(bfs, "BFS")
        elif k == 'd': self.run_algo(dfs, "DFS")
        elif k == 'a': self.run_algo(a_star, "A*")
        elif k == 't': self.run_multi_delivery()
        elif k == 'r': self.reset_sim()

    def reset_sim(self):
        self.grid.reset_viz()
        self.car.reset(self.grid, self.grid.start_pos)
        self.update_stats("RE-INITIALIZED", 0, 0)

    def update_stats(self, status, explored, path_len):
        eff = 100 if path_len > 0 else 0
        self.hud_stats.text = f"<b>SYSTEM METRICS</b>\nStatus: {status}\nNodes: {explored}\nPath: {path_len}"

    def run_algo(self, algo_func, name):
        self.running = True
        self.cursor_obj.visible = False
        self.grid.reset_viz()
        self.car.teleport_to_grid(self.grid, self.grid.start_pos)
        
        start_time = time.time()
        gen = algo_func(self.grid, self.grid.start_pos, self.grid.dest_pos)
        
        path = None
        count = 0
        
        while True:
            try:
                rate(ANIMATION_RATE)
                step = next(gen)
                if step[0] == "visit":
                    self.grid.highlight_visited(step[1])
                    count += 1
            except StopIteration as e:
                path, explored = e.value
                break
        
        end_time = time.time()
        if path:
            self.grid.highlight_path(path)
            for pos in path:
                self.car.move_to_grid(self.grid, pos)
            self.update_stats(f"{name} READY", explored, len(path))
        else:
            self.update_stats(f"{name} BLOCKED", explored, 0)
            
        self.cursor_obj.visible = True
        self.running = False

    def run_multi_delivery(self):
        self.running = True
        self.cursor_obj.visible = False
        self.grid.reset_viz()
        
        # Key Distribution Hubs
        targets = [(2, 2), (GRID_SIZE-3, 2), (2, GRID_SIZE-3)]
        self.grid.multi_targets = targets
        self.grid.reset_viz()
        
        path, explored = optimize_delivery(self.grid, self.grid.start_pos, targets)
        
        if path:
            self.grid.highlight_path(path)
            for pos in path:
                self.car.move_to_grid(self.grid, pos)
            self.update_stats("DELIVERY COMPLETE", explored, len(path))
        
        self.cursor_obj.visible = True
        self.running = False

if __name__ == "__main__":
    app = SimulationApp()
    while True:
        rate(10)
