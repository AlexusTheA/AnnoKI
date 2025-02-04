import numpy as np
import time

q_table = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],      #House
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],      #Fisher
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],      #Woodcutter
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],      #Sheep
                   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])      #Cloth


q_table[:, 1]


actions = np.array(0) + np.array(10, 11, 12, 13, 14) + np.array(20, 21, 22, 23, 24)


num_episodes = 1000

start = 1

# Training
num_episodes = 10000
start_time = time.time()

for episode in range(num_episodes):
    state = start
    done = False
    steps = 0

    print(f"Episode {episode+1} gestartet. Startzustand: {state}")

    while not done:
       
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