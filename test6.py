import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
y = [1, 12, 10, 1, 5, 3, 5, 7, 4, 4]

x_vals = []
y_vals = []

cnt = 0
def animate(i, cnt):
    print(cnt)
    print('loop ' + str(cnt))

    x_vals.append(x[cnt])
    y_vals.append(y[cnt])

    print(x_vals, y_vals)
    cnt += 1  # this is not happening
    plt.plot(x_vals, y_vals, label='Price')

ani = FuncAnimation(plt.gcf(), animate, fargs=(cnt,), interval=1000)

# plt.tight_layout()
plt.show()