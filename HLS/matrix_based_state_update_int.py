import numpy as np
import matplotlib.pyplot as plt

# Parameters
size = 4  # Number of neurons
phase_diff = 90  # Desired phase difference in degrees
frequency = 1.0  # Oscillation frequency (Hz)
dt = 0.01  # Time step (s)
timesteps = 500  # Number of iterations

# Convert phase difference to radians and scale it
phase_diff_rad = np.deg2rad(phase_diff)
scale_factor = 2**16  # Scaling to approximate the phase values as 32-bit integers
output_scale_factor = 2**15  # Scale sine output to integer range

# Initialize state and coupling matrix using integers
states = np.linspace(0, phase_diff_rad * (size - 1), size) * scale_factor
coupling_matrix = np.array([
    [0, 1, 0, -1],
    [-1, 0, 1, 0],
    [0, -1, 0, 1],
    [1, 0, -1, 0]
]) * (0.1 * scale_factor)  # Adjust coupling strength

# Time evolution
outputs = np.zeros((timesteps, size), dtype=np.int32)  # Keep outputs as 32-bit integers
for t in range(timesteps):
    # Update states with coupling (use integer arithmetic and wrap)
    states = states + (2 * np.pi * frequency * dt * scale_factor)  # Integer math
    coupling_effect = np.dot(coupling_matrix, np.sin(states / scale_factor))  # Use sin directly on float
    states += (coupling_effect * dt).astype(np.int32)  # Ensure integer type
    states = np.mod(states, 2 * np.pi * scale_factor)  # Wrap phases to [0, 2π]

    # Store output (convert sine result to integer by scaling)
    outputs[t, :] = (np.sin(states / scale_factor) * output_scale_factor).astype(np.int32)

# Plot outputs for reference
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

# Output file for reference
file_path = "./neuron_outputs_python.txt"
with open(file_path, "w") as f:
    for i in range(size):
        f.write(f"Neuron {i+1} Output Values:\n")
        f.write(f"  {list(outputs[:, i])}\n")
        f.write("\n")
