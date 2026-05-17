import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz

x = np.arange(0, 0.5, 0.01)

low = fuzz.trimf(x, [0, 0, 0.15])
med = fuzz.trimf(x, [0.1, 0.2, 0.3])
high = fuzz.trimf(x, [0.25, 0.5, 0.5])

plt.plot(x, low, label="Low")
plt.plot(x, med, label="Medium")
plt.plot(x, high, label="High")

plt.title("EAR Membership Functions")
plt.legend()
plt.show()