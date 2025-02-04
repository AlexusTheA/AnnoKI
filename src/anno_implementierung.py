import numpy as np
import random
import time
import utils.tool_functions as tf
import Buildings as b

# Grid-World Definition
requirments = {
    "states" : 300,
    "grid_size": (300, 6),  # 2x2 Grid
    "start": 0,
    "goal":  np.array([0, 48, 0, 0, 10, 0, 3])
} 
requirments_states = requirments["states"]

hyperparameter = {
    "alpha": 0.1,      # Lernrate
    "gamma": 0.9,      # Discount-Faktor
    "epsilon": 0.1,    # Explorationsrate
}




# Aktionen: Up, Down, Left, Right
actions = np.concatenate(([0], [1, 2, 4, 5, 6]))

# Q-Table: (Zustände x Aktionen)
q_table = np.zeros((requirments["grid_size"][0] * requirments["grid_size"][1], len(actions)))


def q_learning(q_table, actions, world_grid, hyperparameter, num_episodes):
    grid_size = world_grid["grid_size"]
    start = world_grid["start"]
    next_state = 0
    goal = world_grid["goal"]
    minimal_steps = 300

    #Flags für die Goals
    

    epsilon = hyperparameter["epsilon"]
    alpha = hyperparameter["alpha"]
    gamma = hyperparameter["gamma"]
    start_time = time.time()
    for episode in range(num_episodes):
        Sim = b.GameSimulation()
        flags = 0b100101
        state = start
        done = False
        steps = 0
        while not done:
            # Epsilon-greedy Action Selection
            if random.uniform(0, 1) < epsilon:
                action = random.choice(actions)  # Exploration
            else:
                q_values = q_table[state, actions]
                action = actions[np.argmax(q_values)]  # Exploitation
            Sim.run(action, state)
            next_state = state + 1
            # Belohnung
            reward, flags = tf.reward(requirments["goal"], Sim.resources, flags)
            # Q-Learning-Update
            best_next_action = np.max(q_table[next_state, actions])
            q_table[state, action] += alpha * (reward + gamma * best_next_action - q_table[state, action])
            state = next_state
            steps += 1
            if tf.goal(requirments_states, state, flags):
                minimal_steps = tf.minimal(state, minimal_steps)
                done = True

        
    end_time = time.time()
    return (end_time - start_time), minimal_steps



# Training
learning_time, minimal_steps = q_learning(q_table, actions, requirments, hyperparameter, num_episodes=10000)

"""
# Ausgabe der gelernten Q-Tabelle
for i in range(requirments["grid_size"][0]):
    for j in range(requirments["grid_size"][1]):
        state_idx = tf.state_to_index((i, j), requirments["grid_size"])
        print(f"State ({i},{j}): {q_table[state_idx]}")
"""
# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {learning_time:.2f} Sekunden")

#tf.draw_grid(q_table, requirments["start"], requirments["goal"], requirments["grid_size"], [])

tf.timeline(q_table, minimal_steps)

Sim = b.GameSimulation()
for x in range(300):
    Sim.run(np.argmax(np.ma.masked_equal(q_table[x], 0)), x )

print(Sim.resources)
print(len(Sim.buildings[0]))