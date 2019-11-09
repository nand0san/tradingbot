import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import json
import datetime

y = np.array([8000])
x = np.array(['2019-11-09T20:06:08.426895'])

def f(x, y):

    full_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    binanceTick1 = requests.get(full_url)
    json_response = json.loads(binanceTick1.text)
    price = float(json_response['price'])

    pricing = []
    timestamps = []
    pricing.append(price)
    timestamps.append(datetime.datetime.now().isoformat())

    x = np.concatenate((x, timestamps))
    y = np.concatenate((y, pricing))

    return x, y

x, y = f(x, y)
lines = plt.plot(x, y)
plt.axis([x[0], x[-1], y[0], y[-1]])
plt.xlabel('Time')
plt.ylabel('Price')

# counter = [0]
def animate(i):
    global x, y
    x, y = f(x, y)
    # lines[0].set_ydata(y)
    # # plt.legend(['ts=%4.2f' % ts])
    # #plt.savefig('tmp_%04d.png' % counter)
    # counter[0] += 1

anim = animation.FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.show()
