import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2, 100)
y = np.sin(x)

plt.plot(x, y**2, label='linear')
plt.plot(x, x**2, label='quadratic')
plt.plot(x, x**3, label='cubic')

plt.xlabel('x label')
plt.ylabel('y label')

plt.title("Simple Plot")

plt.legend()

plt.show()
