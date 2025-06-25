# Gait pattern rules
limb_states = [0, 0, 1, 1]  # Initial states: [front_left, front_right, back_left, back_right]

for t in range(20):  # Simulate 20 time steps
    if t % 10 == 0:  # Switch states every 10 steps
        limb_states = [~s for s in limb_states]  # Toggle all limbs

    print(f"Time {t}: {limb_states}")
