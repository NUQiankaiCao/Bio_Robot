import numpy as np
import matplotlib.pyplot as plt

# Parameters
size = 4
phase_diff = 90  # Desired phase difference in degrees
frequency = 1.0  # Oscillation frequency
dt = 0.01  # Time step
timesteps = 5000  # Number of iterations

# Convert phase difference to radians
phase_diff_rad = np.deg2rad(phase_diff)

# Initialize phase and amplitude
phases = np.linspace(0, phase_diff_rad * (size - 1), size)
phases = np.mod(phases, 2 * np.pi)  # Ensure within [0, 2π]
amplitudes = np.ones(size)

# Coupling strength
coupling_strength = 0.1

# Time evolution
outputs = np.zeros((timesteps, size))
for t in range(timesteps):
    # Update phases
    for i in range(size):
        coupling = np.sum(coupling_strength * np.sin(phases - phases[i]))
        phases[i] += 2 * np.pi * frequency * dt + coupling * dt

    # Update amplitudes (optional for amplitude modulation)
    amplitudes = np.ones(size)  # Keep constant or apply a model for dynamics

    # Store output (e.g., amplitude * sine wave of phase)
    outputs[t, :] = amplitudes * np.sin(phases)

# Plot outputs
time = np.arange(timesteps) * dt
for i in range(size):
    plt.plot(time, outputs[:, i], label=f'Neuron {i+1}')
plt.title("CPG Outputs with 90-degree Phase Difference")
plt.xlabel("Time (s)")
plt.ylabel("Neuron Outputs")
plt.legend()
plt.show()

