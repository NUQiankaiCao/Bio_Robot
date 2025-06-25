import numpy as np
import matplotlib.pyplot as plt

# Parameters
size = 4  # Number of oscillators
phase_diff = 90  # Desired phase difference in degrees
dt = 0.01  # Time step
timesteps = 1000  # Number of iterations
frequency = 1.0  # Oscillation frequency (Hz)

# Convert phase difference to radians
phase_diff_rad = np.deg2rad(phase_diff)

# Initialize phases
phases = np.linspace(0, phase_diff_rad * (size - 1), size)
phases = np.mod(phases, 2 * np.pi)  # Ensure within [0, 2π]

# Initialize coupling matrix
weights = np.ones((size, size)) * 0.5  # Uniform coupling strength
np.fill_diagonal(weights, 0)  # No self-coupling

# Time evolution
outputs = np.zeros((timesteps, size))
for t in range(timesteps):
    # Update phases based on coupling
    for i in range(size):
        coupling = np.sum(weights[i, :] * np.sin(phases - phases[i]))
        phases[i] += 2 * np.pi * frequency * dt + coupling * dt

    # Wrap phases back to [0, 2π]
    phases = np.mod(phases, 2 * np.pi)

    # Store output (e.g., sine wave of phase)
    outputs[t, :] = np.sin(phases)

# Plot outputs
time = np.arange(timesteps) * dt
for i in range(size):
    plt.plot(time, outputs[:, i], label=f'Neuron {i+1}')
plt.title("CPG Outputs with 90-degree Phase Difference")
plt.xlabel("Time (s)")
plt.ylabel("Neuron Outputs")
plt.legend()
plt.show()

