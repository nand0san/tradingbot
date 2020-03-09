import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import requests


class ML_predict(object):

    def __init__(self, market, ticks='1m', interval=60, precision=0.95, limit=1000):

        self.market = market
        self.ticks = ticks
        self.interval = interval
        self.precision = precision
        self.limit = limit

        self.df = self.get_data(self.market, self.ticks, self.interval, self.limit)

        # test precision
        if self.test_precision(self.df, self.precision):
            print(f"Precisión satisfactoria!!!!!")
        self.oportunidad = self.predict_oportunity(self.df)

        return

    @staticmethod
    def predict_oportunity(df):
        # predict last price oportunity
        X_train = df.dropna().drop(['predict'], axis=1)
        X_test = df[df.isnull().any(axis=1)].drop(['predict'], axis=1)
        y_train = df['predict'].dropna()
        model = RandomForestRegressor(n_estimators=20)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        sell = pred[-1]  # prediccion del valor actual cuando pase el intervalo calculado
        buy = X_test['close'].iloc[-1]  # valor actual
        print(f"Predicción de oportunidad: {buy} {sell}")
        average = float(sell) / float(buy)
        return float(sell), float(buy), average

    @staticmethod
    def test_precision(df, precision=0.95):
        # calculos de la precision en modo supervisado
        train = df.dropna()  # elimino la parte sin rsultados, ya que estoy en modo supervisado
        X = train.drop(['predict'], axis=1)
        y = train['predict']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=101)
        model_supervised = RandomForestRegressor(n_estimators=20)
        model_supervised.fit(X_train, y_train)
        pred_supervised = model_supervised.predict(X_test)

        r2 = r2_score(y_test, pred_supervised)
        precision_result = model_supervised.score(X_train, y_train)
        print(f'Resultados de precisión: r2 {r2} prec {precision_result}')
        if precision_result >= precision:
            return True
        else:
            return False

    @staticmethod
    def get_data(market, tick='1m', interval=60, limit=1000):
        url_prices = 'https://api.binance.com/api/v1/klines?symbol=' + market + '&interval=' + tick + \
                     '&limit=' + str(limit)
        init_candles = requests.get(url_prices).json()
        df = pd.DataFrame(
            columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close time', 'quote', 'trades',
                     'takers_buy_base', 'takers_buy_quote', 'ignore'])
        for i in range(len(init_candles)):
            df.loc[i] = init_candles[i]
        df['predict'] = df['close'].shift(-interval)
        df = df.drop('ignore', axis=1)
        return df


def main():
    markets = ['BTCUSDT', 'ETHUSDT', 'LINKUSDT', 'BCHUSDT']
    ticks = ['1m', '5m']
    limit = 1000  # 1000 es el maximo de la api
    interval = [120, 60]
    precision = 0.95

    ML_predict(markets[0], ticks[0], interval[1], precision, limit)


if __name__ == '__main__':
    print('Starting process....')
    main()
