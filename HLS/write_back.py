import numpy as np
import matplotlib.pyplot as plt

# Constants
FIXED_SCALE = 2**16  # Scaling factor (65536)
PI = 205887  # Scaled 3.14159265359 * FIXED_SCALE
TWO_PI = 411775  # Scaled 2 * PI
FREQ = 65536  # Scaled 1.0 * FIXED_SCALE (1Hz)
DT = 655  # Scaled 0.01 * FIXED_SCALE

# Maximum value for a signed 32-bit integer
MAX_INT32 = 2**31 - 1
MIN_INT32 = -2**31

# Coupling matrix (scaled)
C_00 = 0; C_01 = 6554; C_02 = 0; C_03 = -6554
C_10 = -6554; C_11 = 0; C_12 = 6554; C_13 = 0
C_20 = 0; C_21 = -6554; C_22 = 0; C_23 = 6554
C_30 = 6554; C_31 = 0; C_32 = -6554; C_33 = 0

# Initial phase states (scaled)
state_0 = 0
state_1 = PI // 2
state_2 = PI
state_3 = (3 * PI) // 2

# Initialize the outputs
outputs_0 = 0
outputs_1 = 0
outputs_2 = 0
outputs_3 = 0

# Sine lookup function (scaled to 16-bit range)
def sin_lookup(phase):
    # Scale phase to the appropriate range
    phase_scaled = phase % TWO_PI  # Keep phase within [0, 2*pi]
    # Calculate sine value in range [-1, 1], then scale to 16-bit integer range [-2^15, 2^15-1]
    sine_value = np.sin(phase_scaled / FIXED_SCALE * 2 * np.pi)
    scaled_value = int(sine_value * (2**15))  # Scale to 16-bit range

    # Clip the value to make sure it stays within the valid signed 16-bit range
    return np.clip(scaled_value, -2**15, 2**15 - 1)

# Function to simulate the clock cycles
def simulate_cpg(timesteps, reset=False):
    global state_0, state_1, state_2, state_3, outputs_0, outputs_1, outputs_2, outputs_3

    outputs = []

    for t in range(timesteps):
        # Reset logic
        if reset:
            state_0 = 0
            state_1 = PI // 2
            state_2 = PI
            state_3 = (3 * PI) // 2
            outputs_0 = 0
            outputs_1 = 0
            outputs_2 = 0
            outputs_3 = 0
            reset = False  # Only reset once at the start

        # Compute coupling sums manually (fixed-point division with shifts)
        coupling_sum_0 = (C_01 * state_1 + C_03 * state_3) >> 16
        coupling_sum_1 = (C_10 * state_0 + C_12 * state_2) >> 16
        coupling_sum_2 = (C_21 * state_1 + C_23 * state_3) >> 16
        coupling_sum_3 = (C_30 * state_0 + C_32 * state_2) >> 16

        # Update states (with fixed-point multiplication and division)
        state_0 += ((FREQ * DT) >> 16) + ((coupling_sum_0 * DT) >> 16)
        state_1 += ((FREQ * DT) >> 16) + ((coupling_sum_1 * DT) >> 16)
        state_2 += ((FREQ * DT) >> 16) + ((coupling_sum_2 * DT) >> 16)
        state_3 += ((FREQ * DT) >> 16) + ((coupling_sum_3 * DT) >> 16)

        # Wrap phase (mod 2π)
        if state_0 >= TWO_PI:
            state_0 -= TWO_PI
        if state_1 >= TWO_PI:
            state_1 -= TWO_PI
        if state_2 >= TWO_PI:
            state_2 -= TWO_PI
        if state_3 >= TWO_PI:
            state_3 -= TWO_PI

        # Generate outputs using sine lookup
        outputs_0 = sin_lookup(state_0)
        outputs_1 = sin_lookup(state_1)
        outputs_2 = sin_lookup(state_2)
        outputs_3 = sin_lookup(state_3)

        # Save the outputs for this clock cycle
        outputs.append([outputs_0, outputs_1, outputs_2, outputs_3])

    return np.array(outputs)

# Simulate for 500 clock cycles (timesteps)
timesteps = 500
reset = True
outputs = simulate_cpg(timesteps, reset)

# Plot the outputs for the four signals
plt.figure(figsize=(10, 6))

# Plot each output on the same graph
plt.plot(outputs[:, 0], label='Output 0')
plt.plot(outputs[:, 1], label='Output 1')
plt.plot(outputs[:, 2], label='Output 2')
plt.plot(outputs[:, 3], label='Output 3')

# Add labels and title
plt.title('CPG Outputs over Time')
plt.xlabel('Time (clock cycles)')
plt.ylabel('Output value')
plt.legend()

# Display the plot
plt.show()
