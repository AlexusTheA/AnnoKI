import numpy as np
import random
import time
import utils.tool_functions as tf
import Buildings as b
from datetime import datetime

# Grid-World Definition
requirments = {
    "states" : 200,
    "grid_size": (200, 6),  # 2x2 Grid
    "start": 0,
    "goal":  np.array([0, 48, 0, 0, 10, 0, 3])
} 
requirments_states = requirments["states"]

hyperparameter = {
    "alpha": 0.2,      # Lernrate
    "gamma": 0.90,      # Discount-Faktor
    "epsilon": 0.1,    # Explorationsrate
}

best = [0 for _ in range(501)]
new_best = []


# Aktionen: Up, Down, Left, Right
actions = np.concatenate(([0], [1, 2, 3, 4, 5, 6]))

# Q-Table: (Zustände x Aktionen)
q_table = np.zeros((requirments["grid_size"][0] * requirments["grid_size"][1], len(actions)))


def q_learning(q_table, actions, world_grid, hyperparameter,new_best, best, num_episodes):
    requirments_states = requirments["states"]
    start = world_grid["start"]
    next_state = 0
    goal = requirments["goal"]
    minimal_steps = 300
    
    
    alpha = hyperparameter["alpha"]
    gamma = hyperparameter["gamma"]
    start_time = time.time()
    for episode in range(num_episodes):
        epsilon = hyperparameter["epsilon"]
        Sim = b.GameSimulation()
        flags = 0b0100101
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
            reward, flags = tf.reward_bin(goal, Sim.resources, flags, action)
            # Q-Learning-Update
            best_next_action = np.max(q_table[next_state, actions])
            q_table[state, action] += alpha * (reward + gamma * best_next_action - q_table[state, action])
            collum = [state, action, Sim.resources.copy(), [len(i) for i in Sim.buildings]]
            new_best.append(collum)
            state = next_state
            steps += 1
            if tf.goal(requirments_states, state, flags):
                
                minimal_steps = tf.minimal(state, minimal_steps)
                done = True

        if len(new_best) < len(best):
            best = new_best
        new_best = []
    end_time = time.time()
    return (end_time - start_time), minimal_steps, best



# Training
learning_time, minimal_steps, best = q_learning(q_table, actions, requirments, hyperparameter, new_best, best, num_episodes=10000)

# Laufzeit anzeigen
print(f"Gesamtlaufzeit: {learning_time:.2f} Sekunden")


#Printen der Timeline
tf.timeline(q_table, 200)
flag = 0b0100101
jetzt = 0
Sim = b.GameSimulation()
while(tf.goal(200, jetzt, flag) != True):
    print(jetzt)
    print(Sim.resources)
    print_a = []
    for i in Sim.buildings:
        print_a.append(len(i))
    print(print_a)
    Sim.run(np.argmax(np.ma.masked_equal(q_table[jetzt], 0)), jetzt )
    reward1, flag = tf.reward_bin(requirments["goal"], Sim.resources, flag, np.argmax(np.ma.masked_equal(q_table[jetzt], 0)))
    jetzt += 1

print(Sim.resources)
print(len(Sim.buildings[0]))


#Txt output der Q-Tabelle
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"liste_{timestamp}.txt"

with open(filename, "w", encoding="utf-8") as file:
    for x in best:
        for i in x:
            if isinstance(i, list):
                file.write(f"{','.join(map(str, i))}    |")  # Liste als String formatieren
            else:
                file.write(f"{i}    |")
        file.write("\n")

print(f"Liste wurde in '{filename}' gespeichert.")

np.savetxt("q_table_matrix.txt", q_table, fmt="%.4f")  # Speichert die Tabelle mit 4 Nachkommastellen
print("Q-Tabelle als Matrix gespeichert.")


filename = "q_table_output.txt"

with open(filename, "w", encoding="utf-8") as file:
    for state, values in enumerate(q_table):
        file.write(f"State {state}: {values}\n")

print(f"Q-Tabelle wurde in '{filename}' gespeichert.")