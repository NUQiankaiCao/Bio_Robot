import numpy as np
import matplotlib.pyplot as plt

# Parameters
size = 4  # Number of neurons
phase_diff = 90  # Desired phase difference in degrees
frequency = 1.0  # Oscillation frequency (Hz)
dt = 0.01  # Time step (s)
timesteps = 500  # Number of iterations

# Convert phase difference to radians
phase_diff_rad = np.deg2rad(phase_diff)

# Initialize state and coupling matrix
states = np.linspace(0, phase_diff_rad * (size - 1), size)
coupling_matrix = np.array([
    [0, 1, 0, -1],
    [-1, 0, 1, 0],
    [0, -1, 0, 1],
    [1, 0, -1, 0]
]) * 0.1  # Adjust coupling strength

# Time evolution
outputs = np.zeros((timesteps, size))
for t in range(timesteps):
    # Update states with coupling
    states += 2 * np.pi * frequency * dt + coupling_matrix @ np.sin(states) * dt
    states = np.mod(states, 2 * np.pi)  # Wrap phases to [0, 2π]

    # Store output
    outputs[t, :] = np.sin(states)

# Plot outputs as separate rows
time = np.arange(timesteps) * dt
fig, axes = plt.subplots(size, 1, figsize=(10, 6), sharex=True, constrained_layout=True)

for i in range(size):
    axes[i].plot(time, outputs[:, i], color=f"C{i}")
    axes[i].set_ylabel(f"N{i+1}", rotation=0, labelpad=20)
    axes[i].set_yticks([])
    axes[i].spines["top"].set_visible(False)
    axes[i].spines["right"].set_visible(False)
    axes[i].spines["left"].set_visible(False)

axes[-1].set_xlabel("Time (s)")
fig.suptitle("CPG Outputs with 90-degree Phase Difference (Flattened View)", y=1.02, fontsize=14)
plt.show()

