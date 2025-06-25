import numpy as np
import matplotlib.pyplot as plt

# Parameters
size = 20  # Number of degrees of freedom (neurons)
phase_diff = 90  # Desired phase difference in degrees
frequency = 1.0  # Oscillation frequency (Hz)
dt = 0.01  # Time step (s)
timesteps = 500  # Number of iterations

# Convert phase difference to radians
phase_diff_rad = np.deg2rad(phase_diff)

# Initialize state and coupling matrix
states = np.linspace(0, phase_diff_rad * (size - 1), size) % (2 * np.pi)
coupling_strength = 0.05  # Adjust coupling strength
coupling_matrix = np.zeros((size, size))

# Define a cyclic coupling pattern
for i in range(size):
    coupling_matrix[i, (i + 1) % size] = coupling_strength  # Forward neighbor
    coupling_matrix[i, (i - 1) % size] = -coupling_strength  # Backward neighbor

# Time evolution
outputs = np.zeros((timesteps, size))
for t in range(timesteps):
    # Update states with coupling
    states += 2 * np.pi * frequency * dt + coupling_matrix @ np.sin(states) * dt
    states = np.mod(states, 2 * np.pi)  # Wrap phases to [0, 2π]

    # Store output
    outputs[t, :] = np.sin(states)

# Plot outputs as 20 rows
time = np.arange(timesteps) * dt
fig, axes = plt.subplots(size, 1, figsize=(12, 10), sharex=True, constrained_layout=True)

for i in range(size):
    axes[i].plot(time, outputs[:, i], color=f"C{i}")
    axes[i].set_ylabel(f"N{i+1}", rotation=0, labelpad=20)
    axes[i].set_yticks([])
    axes[i].spines["top"].set_visible(False)
    axes[i].spines["right"].set_visible(False)
    axes[i].spines["left"].set_visible(False)

axes[-1].set_xlabel("Time (s)")
fig.suptitle("CPG Outputs with 20 Degrees of Freedom (Flattened View)", y=1.02, fontsize=16)
plt.show()

