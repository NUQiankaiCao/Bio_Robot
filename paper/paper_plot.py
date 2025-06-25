import numpy as np
import matplotlib.pyplot as plt

# Parameters
frequency = 1          # Frequency in Hz
amplitude = 1          # Amplitude of the sine wave
sampling_rate = 1000   # Samples per second
duration = 2           # Duration in seconds

# Time array
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Phase shifts in degrees and corresponding colors
phase_shifts = [0, 90, 180, 270]
colors = ['green', 'red', 'blue', 'yellow']

# Generate and plot the sine waves
plt.figure(figsize=(10, 5))
for phase, color in zip(phase_shifts, colors):
    y = amplitude * np.sin(2 * np.pi * frequency * t + np.deg2rad(phase))
    # plt.plot(t, y, label=f'{phase}° phase', color=color)
    plt.plot(t, y, color=color,linewidth=4)

plt.title('Sine Waves with 90° Phase Differences')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

