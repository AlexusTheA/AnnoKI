import numpy as np
import random
import time
import utils.tool_functions as tf

# Grid-World Definition
world_grid = {
    "grid_size": (6, 6),  # 2x2 Grid
    "start": (0, 0),
    "goal": (5, 5)
}
hyperparameter = {
    "alpha": 0.1,      # Lernrate
    "gamma": 0.9,      # Discount-Faktor
    "epsilon": 0.1    # Explorationsrate
}
# Aktionen: Up, Down, Left, Right
actions = {0: (-1, 0), 1: (1, 0), 2: (0, -1), 3: (0, 1)}
# Q-Table: (Zustände x Aktionen)
q_table = np.zeros((world_grid["grid_size"][0] * world_grid["grid_size"][1], len(actions)))


def q_learning(q_table, actions, world_grid, hyperparameter, num_episodes):
    grid_size = world_grid["grid_size"]
    start = world_grid["start"]
    goal = world_grid["goal"]

    epsilon = hyperparameter["epsilon"]
    alpha = hyperparameter["alpha"]
    gamma = hyperparameter["gamma"]
    start_time = time.time()
    for episode in range(num_episodes):
        state = start
        done = False
        steps = 0
        while not done:
            state_idx = tf.state_to_index(state, grid_size)
            valid_actions = tf.get_valid_actions(state, actions, grid_size)
            # Epsilon-greedy Action Selection
            if random.uniform(0, 1) < epsilon:
                action = random.choice(valid_actions)  # Exploration
            else:
                q_values = q_table[state_idx, valid_actions]
                action = valid_actions[np.argmax(q_values)]  # Exploitation
            move = actions[action]
            next_state = (state[0] + move[0], state[1] + move[1])
            next_state_idx = tf.state_to_index(next_state, grid_size)
            # Belohnung
            reward = 10 if next_state == goal else -1
            # Q-Learning-Update
            best_next_action = np.max(q_table[next_state_idx, tf.get_valid_actions(next_state, actions, grid_size)])
            q_table[state_idx, action] += alpha * (reward + gamma * best_next_action - q_table[state_idx, action])
            state = next_state
            steps += 1
            if state == goal:
                done = True
    end_time = time.time()
    return (end_time - start_time)



# Training
learning_time = q_learning(q_table, actions, world_grid, hyperparameter, num_episodes=1000)


# Ausgabe der gelernten Q-Tabelle
for i in range(world_grid["grid_size"][0]):
    for j in range(world_grid["grid_size"][1]):
        state_idx = tf.state_to_index((i, j), world_grid["grid_size"])
        print(f"State ({i},{j}): {q_table[state_idx]}")

# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {learning_time:.2f} Sekunden")

tf.draw_grid(q_table, world_grid["start"], world_grid["goal"], world_grid["grid_size"], [])