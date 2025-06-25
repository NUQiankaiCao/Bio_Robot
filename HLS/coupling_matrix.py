import numpy as np

def generate_coupling_matrix(size, phase_diff):
    # Generate a matrix with sinusoidal phase shifts
    phase_diff_rad = np.deg2rad(phase_diff)
    W = np.zeros((size, size))
    for i in range(size):
        for j in range(size):
            W[i, j] = np.sin(phase_diff_rad * (i - j))
    return W

# Example for 4 oscillators with 90-degree phase difference
W = generate_coupling_matrix(4, 90)
print(W)

