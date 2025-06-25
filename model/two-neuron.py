# Python-like pseudocode
state_A = 0  # Initial state of neuron A
state_B = 1  # Initial state of neuron B
threshold = 0.5
time_step = 0.1
coupling_strength = 0.2

for t in range(100):  # Simulate 100 time steps
    # Update states based on inhibitory coupling
    new_state_A = max(0, 1 - coupling_strength * state_B)
    new_state_B = max(0, 1 - coupling_strength * state_A)

    # Apply threshold for oscillation
    state_A = 1 if new_state_A > threshold else 0
    state_B = 1 if new_state_B > threshold else 0

    print(f"Time: {t * time_step}, A: {state_A}, B: {state_B}")

