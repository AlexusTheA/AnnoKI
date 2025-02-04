import numpy as np
import random
import os


# Farben für die Darstellung
COLORS = {
    'start': '\033[93m',  # Gelb
    'goal': '\033[92m',   # Grün
    'path': '\033[92m',   # Grün
    'pit': '\033[30m',   # Grün
    'empty': '\033[91m',  # Rot
    'reset': '\033[0m'    # Zurücksetzen der Farbe
}


def generate_maze(width, height):
    grid = [['#' for _ in range(width)] for _ in range(height)]
    start_x, start_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    grid[start_y][start_x] = 'S'  # Startpunkt
    walls = [(start_x + dx, start_y + dy, start_x + 2*dx, start_y + 2*dy) 
             for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
             if 0 < start_x + 2*dx < width and 0 < start_y + 2*dy < height]
    
    while walls:
        wx, wy, nx, ny = random.choice(walls)
        walls.remove((wx, wy, nx, ny))
        
        if grid[ny][nx] == '#':
            grid[wy][wx] = ' '
            grid[ny][nx] = ' '
            walls.extend([(nx + dx, ny + dy, nx + 2*dx, ny + 2*dy) 
                          for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                          if 0 < nx + 2*dx < width and 0 < ny + 2*dy < height])
    
    # Set end point
    end_x, end_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    while (end_x, end_y) == (start_x, start_y):
        end_x, end_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    grid[end_y][end_x] = 'E'
    
    return grid, (start_x, start_y), (end_x, end_y)


def state_to_index(state, grid_size):
    return state[0] * grid_size[1] + state[1]

def is_valid_move(state, action, grid_size):
    new_state = (state[0] + action[0], state[1] + action[1])
    return 0 <= new_state[0] < grid_size[0] and 0 <= new_state[1] < grid_size[1]

def get_valid_actions(state, actions, grid_size):
    return [a for a, move in actions.items() if is_valid_move(state, move, grid_size)]

# Funktion zur Darstellung des Grids
def draw_grid(q_table, start, goal, grid_size, pit):
    grid = np.zeros(grid_size, dtype=object)
    
    # Pfad ermitteln
    current_state = start
    current_state_idx = state_to_index(start, grid_size)
    path = [current_state]
    while current_state != goal:
        print(current_state)
        print(current_state_idx)
        action = np.argmax(np.ma.masked_equal(q_table[current_state_idx], 0))
        print(action)
        if action == 0:
            next_state = (current_state[0] - 1, current_state[1])
        elif action == 1:
            next_state = (current_state[0] + 1, current_state[1])
        elif action == 2:
            next_state = (current_state[0], current_state[1] - 1)
        elif action == 3:
            next_state = (current_state[0], current_state[1] + 1)
        else:
            break
        #print(current_state)
        if next_state in path:
            print("Fail")
            break
        path.append(next_state)
        
        if next_state == goal:
            break
        current_state = next_state
        current_state_idx = state_to_index(current_state, grid_size)
    
    # Grid füllen
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            if (j, i) == start:
                grid[i, j] = f"{COLORS['start']}S{COLORS['reset']}"
            elif (j, i) == goal:
                grid[i, j] = f"{COLORS['goal']}G{COLORS['reset']}"
            elif (j, i) in path:
                grid[i, j] = f"{COLORS['path']}P{COLORS['reset']}"
            elif (j, i) in pit:
                grid[i, j] = f"{COLORS['pit']}O{COLORS['reset']}"
            else:
                grid[i, j] = f"{COLORS['empty']}X{COLORS['reset']}"
    
    # Grid ausgeben
    for row in grid:
        print(" ".join(row))


def clear_console():
    # Überprüft das Betriebssystem
    if os.name == 'nt':  # Für Windows
        os.system('cls')
    else:                # Für Linux, macOS, etc.
        os.system('clear')

version = '0.1'