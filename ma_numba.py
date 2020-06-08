import pandas as pd
import numpy as np
import numba


def buy_sell_sl(arr_prices_ma_short_ma_long, qty_btc=0, qty_pair=1000, sl=2):

    flag = -1
    trades = 0
    length = arr_prices_ma_short_ma_long.shape[0]
    price_arr = np.zeros([length, 1])
    sl_arr = np.zeros([length, 1])

    qty_btc_arr = np.zeros([length, 1])
    qty_pair_arr = qty_pair  # wallet initial money i. e. usdt

    for i in arr_prices_ma_short_ma_long.shape[0]:
        if arr_prices_ma_short_ma_long[i][1] > arr_prices_ma_short_ma_long[i][2]:  # compra
            if flag != 1:
                trades += 1
                sl_arr[i:] = arr_prices_ma_short_ma_long[i][0] * ((100 - sl) / 100)  # genero stop loss
                price_arr[i:] = arr_prices_ma_short_ma_long[i][0]  # guardo el precio
                qty_btc_arr[i:] = qty_pair / arr_prices_ma_short_ma_long[i][0] * .99  # obtengo btc
                qty_pair_arr[i:] = 0
                flag = 1

            elif (flag == 1) & (arr_prices_ma_short_ma_long[i][0] <= sl_arr[i]):  # salta stop_loss y vende
                trades += 1
                price_arr[i:] = arr_prices_ma_short_ma_long[i][0]  # guardo el precio
                sl_arr[i:] = 0  # borro stop loss
                qty_pair_arr[i:] = qty_btc[i] * arr_prices_ma_short_ma_long[i][0] * .99
                qty_btc_arr[i:] = 0
                flag = 0


        elif arr_prices_ma_short_ma_long[i][1] < arr_prices_ma_short_ma_long[i][2]:  # vende
            if flag == 1:
                trades += 1
                price_arr[i:] = arr_prices_ma_short_ma_long[i][0]  # guardo el precio
                sl_arr[i:] = 0  # borro stop loss
                qty_pair_arr[i:] = qty_btc[i] * arr_prices_ma_short_ma_long[i][0] * .99
                qty_btc_arr[i:] = 0
                flag = 0

    return price_arr, sl_arr, qty_pair_arr, qty_btc_arr, trades


def ma_array(price_arr):

    
    return price_arr


if __name__ == '__main__':

    df = pd.read_csv('BTCUSDT_historical_trades_03.csv')
    df['time'] = pd.to_datetime(df['time'], unit='ms').dt.tz_localize('utc').dt.tz_convert('Europe/Madrid')
    df = df.set_index('id')  # dejodesindexado para que las llamadas iloc funcionen
    df = df.sort_index()

    price_arr = df['price'].to_numpy()

    ma_array(price_arr)
