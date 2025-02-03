import numpy as np
import random
import time

# Grid-World Definition
grid_size = (3, 2)  # 2x2 Grid
start = (0, 0)
goal = (2, 1)

# Aktionen: Up, Down, Left, Right
actions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}

# Q-Table: (Zustände x Aktionen)
q_table = np.zeros((grid_size[0] * grid_size[1], len(actions)))

# Hyperparameter
alpha = 0.1      # Lernrate
gamma = 0.9      # Discount-Faktor
epsilon = 0.1    # Explorationsrate

# Erlaubte Pfade 
allowed_paths = [(0, 0), (1, 0), (1, 1), (2, 1)]

# Hilfsfunktionen
def state_to_index(state):
    return state[0] * grid_size[1] + state[1]

def is_valid_move(state, action):
    new_state = (state[0] + action[0], state[1] + action[1])
    return new_state in allowed_paths

def get_valid_actions(state):
    return [a for a, move in actions.items() if is_valid_move(state, move)]

# Training
num_episodes = 10000
start_time = time.time()

for episode in range(num_episodes):
    state = start
    done = False
    steps = 0

    print(f"Episode {episode+1} gestartet. Startzustand: {state}")

    while not done:
        state_idx = state_to_index(state)
        valid_actions = get_valid_actions(state)

        # Epsilon-greedy Action Selection
        if random.uniform(0, 1) < epsilon:
            action = random.choice(valid_actions)  # Exploration
            print(f"  Zufällige Aktion gewählt: {action}")
        else:
            q_values = q_table[state_idx, valid_actions]
            action = valid_actions[np.argmax(q_values)]  # Exploitation
            print(f"  Beste bekannte Aktion gewählt: {action}")

        move = actions[action]
        next_state = (state[0] + move[0], state[1] + move[1])
        next_state_idx = state_to_index(next_state)

        # Belohnung
        reward = 10 if next_state == goal else -1

        # Q-Learning-Update
        best_next_action = np.max(q_table[next_state_idx, get_valid_actions(next_state)])
        q_table[state_idx, action] += alpha * (reward + gamma * best_next_action - q_table[state_idx, action])

        print(f"    Von {state} nach {next_state} bewegt. Belohnung: {reward}")

        state = next_state
        steps += 1

        if state == goal:
            done = True
            print(f"Ziel erreicht in {steps} Schritten!\n")

end_time = time.time()

# Ausgabe der gelernten Q-Tabelle
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        state_idx = state_to_index((i, j))
        print(f"State ({i},{j}): {q_table[state_idx]}")

# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {end_time - start_time:.2f} Sekunden")
