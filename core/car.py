from vpython import box, compound, vector, color, rate, cylinder, local_light, sphere
from utils.constants import COLOR_CAR_BODY, CELL_SIZE, CAR_SPEED, COLOR_WHEEL

class Car:
    def __init__(self, start_pos_3d):
        # High-Fidelity Detailed Body
        body = box(pos=vector(0, 0.2, 0), 
                   size=vector(CELL_SIZE * 0.72, 0.24, CELL_SIZE * 0.46), 
                   color=COLOR_CAR_BODY, shininess=1.0)
        
        # Transparent Glass Cabin
        glass = box(pos=vector(-0.04, 0.4, 0), 
                    size=vector(CELL_SIZE * 0.42, 0.22, CELL_SIZE * 0.42), 
                    color=color.white, opacity=0.3, shininess=1.0)
        
        # Wheels with spokes detail (simplified)
        w_radius = 0.14
        wheels = []
        for x in [-0.22, 0.22]:
            for z in [-0.22, 0.22]:
                w = cylinder(pos=vector(x*CELL_SIZE, 0.1, z*CELL_SIZE), 
                             axis=vector(0, 0, 0.06 if z > 0 else -0.06), 
                             radius=w_radius, color=COLOR_WHEEL)
                wheels.append(w)
        
        # Headlights components
        h1 = sphere(pos=vector(0.36 * CELL_SIZE, 0.2, 0.16 * CELL_SIZE), radius=0.08, color=color.white, emissive=True)
        h2 = sphere(pos=vector(0.36 * CELL_SIZE, 0.2, -0.16 * CELL_SIZE), radius=0.08, color=color.white, emissive=True)
        
        # Tail lights components
        t1 = box(pos=vector(-0.36 * CELL_SIZE, 0.2, 0.16 * CELL_SIZE), size=vector(0.04, 0.12, 0.18), color=color.red, emissive=True)
        t2 = box(pos=vector(-0.36 * CELL_SIZE, 0.2, -0.16 * CELL_SIZE), size=vector(0.04, 0.12, 0.18), color=color.red, emissive=True)

        self.visual = compound([body, glass, h1, h2, t1, t2] + wheels)
        self.visual.pos = vector(start_pos_3d.x, 0.2, start_pos_3d.z)
        
        # High-Intensity Dynamic Headlights
        self.l1 = local_light(pos=self.visual.pos + vector(0.5, 0.2, 0.2), color=color.white)
        self.l2 = local_light(pos=self.visual.pos + vector(0.5, 0.2, -0.2), color=color.white)
        
        self.current_grid_pos = (0, 0)

    def move_to_grid(self, grid, target_grid_pos):
        target_3d = grid.get_3d_pos(target_grid_pos)
        target_pos = vector(target_3d.x, 0.2, target_3d.z)
        start_pos = self.visual.pos
        
        dist_vec = target_pos - start_pos
        dist = dist_vec.mag
        
        if dist < 0.01: return
        
        steps = max(1, int(dist / CAR_SPEED))
        direction = dist_vec / steps
        
        # Smooth Rotation to face target
        self.visual.axis = direction
        
        for _ in range(steps):
            rate(60)
            self.visual.pos += direction
            # Precise Light Tracking
            offset_fwd = self.visual.axis * 0.5
            self.l1.pos = self.visual.pos + offset_fwd + vector(0, 0.2, 0.2)
            self.l2.pos = self.visual.pos + offset_fwd + vector(0, 0.2, -0.2)
            
        self.visual.pos = target_pos
        self.current_grid_pos = target_grid_pos

    def teleport_to_grid(self, grid, target_grid_pos):
        target_3d = grid.get_3d_pos(target_grid_pos)
        self.visual.pos = vector(target_3d.x, 0.2, target_3d.z)
        self.current_grid_pos = target_grid_pos
        self.l1.pos = self.visual.pos + vector(0.5, 0.2, 0.2)
        self.l2.pos = self.visual.pos + vector(0.5, 0.2, -0.2)

    def reset(self, grid, start_pos):
        self.teleport_to_grid(grid, start_pos)
