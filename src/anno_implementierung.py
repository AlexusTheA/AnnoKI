import numpy as np
import random
import time
import utils.tool_functions as tf

# Grid-World Definition
requirments = {
    "states" : 300,
    "grid_size": (300, 6),  # 2x2 Grid
    "start": 0,
    "goal":  (48, 0, 0, 10, 0, 3)
} 

hyperparameter = {
    "alpha": 0.1,      # Lernrate
    "gamma": 0.9,      # Discount-Faktor
    "epsilon": 0.1    # Explorationsrate
}

#Flags für die Goals
FLAGS = 0b111

# Aktionen: Up, Down, Left, Right
actions = np.array(0) + np.array(1, 2, 3, 4, 5)

# Q-Table: (Zustände x Aktionen)
q_table = np.zeros((requirments["grid_size"][0] * requirments["grid_size"][1], len(actions)))


def q_learning(q_table, actions, world_grid, hyperparameter, num_episodes, resources):
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
            # Epsilon-greedy Action Selection
            if random.uniform(0, 1) < epsilon:
                action = random.choice(actions)  # Exploration
            else:
                q_values = q_table[state_idx, actions]
                action = actions[np.argmax(q_values)]  # Exploitation
            move = actions[action]
            next_state += state
            # Belohnung
            reward, FLAGS = reward(FLAGS)
            # Q-Learning-Update
            best_next_action = np.max(q_table[next_state, actions])
            q_table[state, action] += alpha * (reward + gamma * best_next_action - q_table[state, action])
            state = next_state
            steps += 1
            if tf.goal(requirments, state, resources):
                done = True
    end_time = time.time()
    return (end_time - start_time)



# Training
learning_time = q_learning(q_table, actions, requirments, hyperparameter, num_episodes=1000)


# Ausgabe der gelernten Q-Tabelle
for i in range(requirments["grid_size"][0]):
    for j in range(requirments["grid_size"][1]):
        state_idx = tf.state_to_index((i, j), requirments["grid_size"])
        print(f"State ({i},{j}): {q_table[state_idx]}")

# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {learning_time:.2f} Sekunden")

tf.draw_grid(q_table, requirments["start"], requirments["goal"], requirments["grid_size"], [])


