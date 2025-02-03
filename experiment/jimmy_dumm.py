import matplotlib.pyplot as plt
import numpy as np
import random
import time
import os
import tool_functions_experiment as tf

# Start- und Zielzustand
start = (2, 18)
goal = (19, 2)
grid_size = (50, 50)

# Farben für die Darstellung
COLORS = {
    'start': '\033[93m',  # Gelb
    'goal': '\033[92m',   # Grün
    'path': '\033[92m',   # Grün
    'pit': '\033[30m',   # Grün
    'empty': '\033[91m',  # Rot
    'reset': '\033[0m'    # Zurücksetzen der Farbe
}



# Labyrinth generieren
maze, start, end = tf.generate_maze(grid_size[0], grid_size[1])

goal = end 


# Blockierte Positionen ermitteln
pit = [(x, y) for y in range(20) for x in range(20) if maze[y][x] == '#']



#pit = [(2, y) for y in range(2, grid_size[1] - 2)] + [(x, 2) for x in range(2, grid_size[0] - 2)]

# Aktionen: Up, Down, Left, Right
actions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

# Dynamische Q-Tabelle als Dictionary
q_table = {}

# Hyperparameter
alpha = 0.1      # Lernrate
gamma = 0.9      # Discount-Faktor
epsilon = 0.1    # Explorationsrate



# Training
num_episodes = 50000
start_time = time.time()
a = 0

for episode in range(num_episodes):
    state = start
    previous_state = (-1, -1)
    done = False
    steps = 0

    tf.initialize_state(state, previous_state, q_table, actions, grid_size)
    #print(f"Episode {episode+1} gestartet. Startzustand: {state}")

    while not done:
        valid_actions = tf.get_valid_actions(state, previous_state, actions, grid_size)

        # Epsilon-greedy Action Selection
        if random.uniform(0, 1) < epsilon:
            action = random.choice(valid_actions)  # Exploration
            #print(f"  Zufällige Aktion gewählt: {action}")
        else:
            q_values = q_table[state]
            action = max(q_values, key=q_values.get)  # Exploitation
            #print(f"  Beste bekannte Aktion gewählt: {action}")

        move = actions[action]
        next_state = (state[0] + move[0], state[1] + move[1])
        tf.initialize_state(next_state, previous_state, q_table, actions, grid_size)

        # Belohnung
        reward = (100 if next_state == goal else -1) + (-100 if any(tuple == next_state for tuple in pit) else 0)

        # Q-Learning-Update
        best_next_action = max(q_table[next_state].values(), default=0)
        q_table[state][action] += alpha * (reward + gamma * best_next_action - q_table[state][action])

        #print(f"    Von {state} nach {next_state} bewegt. Belohnung: {reward}")


        previous_state = state
        state = next_state
        steps += 1

        if state == goal:
            done = True
            #print(f"Ziel erreicht in {steps} Schritten!\n")

    a += 1
    if a % 1000 == 0:
        print(f"Step {a} Done")
        tf.clear_console()
        tf.draw_grid(q_table, start, goal, grid_size, pit)


end_time = time.time()

# Ausgabe der gelernten Q-Tabelle

"""
for state, actions_q in q_table.items():
    print(f"State {state}: {actions_q}")
"""

# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {end_time - start_time:.2f} Sekunden")

# Dateiname
filename = "q_table.txt"

# Speicherort und Dateiname
filepath = r"C:\Users\alex5\Desktop\Anno KI\q_table.txt"

# Q-Tabelle in eine Datei schreiben
with open(filepath, "w") as file:
    for state, actions in q_table.items():
        # Zustand schreiben (z. B. "(0, 0)")
        file.write(f"{state}:\n")
        # Aktionen schreiben (z. B. "0: 1.0, 1: 2.0, ...")
        for action, value in actions.items():
            file.write(f"  {action}: {value}\n")
        file.write("\n")  # Leerzeile zwischen den Zuständen

print(f"Q-Tabelle wurde in '{filepath}' gespeichert.")


# Grid Größe, Start und Ziel
# Funktion zur Ermittlung der Grid-Größe
#def get_grid_size(q_table):
#    max_x = max(state[0] for state in q_table.keys()) + 1
#    max_y = max(state[1] for state in q_table.keys()) + 1
#    return (max_y, max_x)  # (Zeilen, Spalten)

#grid_size = get_grid_size(q_table)



# Beispiel Q-Tabelle


# Grid zeichnen
tf.draw_grid(q_table, start, goal, grid_size, pit)
