import numpy as np
import matplotlib.pyplot as plt

# Constants (Higher Precision)
FIXED_SCALE = 2**20  # Increase precision
PI = int(3.14159265359 * FIXED_SCALE)
TWO_PI = 2 * PI
FREQ = int(1.0 * FIXED_SCALE)  # 1 Hz
DT = int(0.01 * FIXED_SCALE)  # 0.01s

# Initialize phase states (scaled)
state_0 = 0
state_1 = PI // 2
state_2 = PI
state_3 = (3 * PI) // 2

# Coupling matrix (scaled)
C = np.array([
    [0, 65536, 0, -65536],
    [-65536, 0, 65536, 0],
    [0, -65536, 0, 65536],
    [65536, 0, -65536, 0]
])

# Time evolution
timesteps = 1000  # Extended to check for drift
outputs = np.zeros((timesteps, 4))

for t in range(timesteps):
    # Compute coupling sums with higher precision
    coupling_sum_0 = (C[0][1] * state_1 + C[0][3] * state_3) // FIXED_SCALE
    coupling_sum_1 = (C[1][0] * state_0 + C[1][2] * state_2) // FIXED_SCALE
    coupling_sum_2 = (C[2][1] * state_1 + C[2][3] * state_3) // FIXED_SCALE
    coupling_sum_3 = (C[3][0] * state_0 + C[3][2] * state_2) // FIXED_SCALE

    # Update states with higher precision
    state_0 = (state_0 + (FREQ * DT) // FIXED_SCALE + (coupling_sum_0 * DT) // FIXED_SCALE) % TWO_PI
    state_1 = (state_1 + (FREQ * DT) // FIXED_SCALE + (coupling_sum_1 * DT) // FIXED_SCALE) % TWO_PI
    state_2 = (state_2 + (FREQ * DT) // FIXED_SCALE + (coupling_sum_2 * DT) // FIXED_SCALE) % TWO_PI
    state_3 = (state_3 + (FREQ * DT) // FIXED_SCALE + (coupling_sum_3 * DT) // FIXED_SCALE) % TWO_PI

    # Generate outputs using sine lookup
    outputs[t, 0] = np.sin(state_0 / FIXED_SCALE * 2 * np.pi)
    outputs[t, 1] = np.sin(state_1 / FIXED_SCALE * 2 * np.pi)
    outputs[t, 2] = np.sin(state_2 / FIXED_SCALE * 2 * np.pi)
    outputs[t, 3] = np.sin(state_3 / FIXED_SCALE * 2 * np.pi)

# Plot outputs
time = np.arange(timesteps) * (DT / FIXED_SCALE)
plt.figure(figsize=(10, 6))

# for i in range(4):
#     plt.plot(time, outputs[:, i], label=f'Neuron {i+1}')
plt.plot(time, outputs[:, 1], label=f'Neuron {1+1}')
plt.title("CPG Outputs (Corrected for Long-Term Stability)")
plt.xlabel("Time (s)")
plt.ylabel("Neuron Outputs")
plt.legend()
plt.show()
