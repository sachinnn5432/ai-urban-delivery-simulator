from vpython import vector, color, textures

# Grid Settings
GRID_SIZE = 15
CELL_SIZE = 1.0

# Ultra-Realistic Urban Palette
COLOR_ROAD = vector(0.12, 0.12, 0.14)      # Dark Asphalt
COLOR_MARKING = vector(0.7, 0.6, 0.1)      # Weathered Yellow
COLOR_OBSTACLE = vector(0.25, 0.25, 0.25)  # Concrete Rough
COLOR_START = vector(0.0, 0.8, 0.2)        # Modern Traffic Green
COLOR_DESTINATION = vector(0.9, 0.1, 0.1)  # Stop Red
COLOR_CAR_BODY = vector(0.08, 0.08, 0.1)   # Obsidian Metallic
COLOR_WHEEL = vector(0.05, 0.05, 0.05)
COLOR_LAMP_POST = vector(0.1, 0.1, 0.1)
COLOR_LAMP_WARM = vector(1.0, 0.8, 0.4)    # Sodium Vapor Warmth
COLOR_SKY = vector(0.02, 0.02, 0.05)       # Twilight Depth
COLOR_PATH = vector(0.6, 0.5, 0.0)         # Matte Safety Yellow
COLOR_CURSOR = vector(0.0, 1.0, 1.0)       # Cyber Cyan
COLOR_WINDOW = vector(0.9, 0.9, 0.7)       # Light from building windows

# UI Styling
SCENE_WIDTH = 1200
SCENE_HEIGHT = 800

# Speeds
ANIMATION_RATE = 20
CAR_SPEED = 0.18
