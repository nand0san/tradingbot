import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from multiprocessing import Process, Queue
import time

style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
xs = []
ys = []

def animate(i):
    x = []
    y = []
    # while True:
    data = com1.get()
    print(f'Queue get x: {data}')
    for point in data:
        x.append(point[0])
        y.append(point[1])
    data = []
    ax1.clear()
    ax1.plot(x, y)

        # except Queue.empty():
        #     time.sleep(0.25)

def read_data():
    a = []
    b = []
    parsed_line = []
    while True:
        data = open('example.csv', 'r').read()
        lines = data.split('\n')
        for line in lines:
            print(f'Line: {line}')
            if len(line) > 1:
                line_splitted = line.split(',')
                print(f'Splitted: {line_splitted}')
                a.append(int(line_splitted[0]))
                a.append(int(line_splitted[1]))
                parsed_line.append(a)
                a = []
        print(f'To the queue: {parsed_line}')
        com1.put(parsed_line)
        parsed_line = []
        time.sleep(1)


com1 = Queue()
# com2 = Queue()

p1 = Process(target=read_data)
# print('Started process 1: ')
p1.start()
ani = animation.FuncAnimation(fig, animate, interval=1000)

plt.show()
