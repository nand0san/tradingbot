# espera una lista de precios string ordenados cronologicamente, da el resultado del rsi para el ultimo
# precio con respecto a los anteriores

def get_rsi(prices):

    print(prices)
    lastprice = float(prices[0])
    up = []
    down = []

    for price in prices:
        increment = float(price) - lastprice
        if increment > 0:
            up.append(increment)
        elif increment < 0:
            down.append(abs(increment))
        lastprice = price

    up_average = sum(up) / len(up)
    # print(f'Media de las up: {up_average}')
    down_average = sum(down) / len(down)
    # print(f'Media de las down: {down_average}')


    rs = up_average / down_average
    _rsi = 100 - (100/(1. + rs))

    return _rsi

# ## test
# a   = [6971.73, 6937.08, 8218.05, 9251.27, 8870.82, 9114.72, 10226.86, 10107.26, 11233.95, 11767.74, 11459.71, 11104.2, 11175.87, 11429.02]
# print(rsi(a))
