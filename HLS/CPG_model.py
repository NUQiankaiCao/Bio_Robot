from scipy.integrate import odeint

def oscillator(y, t, weights, biases, time_constants):
    dydt = []
    for i in range(len(y)):
        coupling = sum(weights[i][j] * np.sin(y[j] - y[i]) for j in range(len(y)))
        dydt.append((biases[i] + coupling - y[i]) / time_constants[i])
    return dydt

# Initialize parameters
size = 4
biases = np.zeros(size)
time_constants = np.ones(size) * 1.5
weights = generate_coupling_matrix(size, 90)

# Initial conditions
y0 = np.linspace(0, np.pi / 2, size)
t = np.linspace(0, 10, 1000)

# Simulate
outputs = odeint(oscillator, y0, t, args=(weights, biases, time_constants))

