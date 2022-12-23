import json
import requests
import pandas as pd
import datetime


BACKEND_URL = 'http://moex:8080'


class Strategy:
    def __init__(self):
        self.long_pos = False
        self.long_entry_price = 0
        self.short_pos = False
        self.short_entry_price = 0

        self.buy_price = None
        self.short_price = None
        self.sell_price = None
        self.cover_price = None
        self.long_stop_price = None
        self.short_stop_price = None

        self.long_highest = None
        self.long_lowest = None
        self.long_atr = None

        self.short_highest = None
        self.short_lowest = None
        self.short_atr = None

        settings = open('setting.json')
        self.params = json.load(settings)
        self.candles = None

        self.ticker = '???'

    def get_candles(self, ticker, start_date, end_date):
        exchange_name = 'moex'
        time_frame = 'M1'
        params = {
            'exchangeName': exchange_name,
            'timeframe': time_frame,
            'till': end_date,
            'from': start_date
        }
        result = requests.get(BACKEND_URL + '/data/' + ticker, params=params)
        self.candles = pd.DataFrame.from_records(result.text)

    def get_candle(self, ticker):
        exchange_name = 'moex'
        time_frame = 'M1'
        params = {
            'exchangeName': exchange_name,
            'timeframe': time_frame,
        }
        result = requests.get(BACKEND_URL + '/data/' + ticker, params=params)
        df = pd.DataFrame.from_records(result.text)
        self.candles = self.candles.append(df, ignore_index=True)

    def get_atr(self):
        self.candles['tr0'] = abs(self.candles['HIGH'] - self.candles['LOW'])
        self.candles['tr1'] = abs(self.candles['HIGH'] - self.candles['CLOSE'].shift())
        self.candles['tr2'] = abs(self.candles['LOW'] - self.candles['CLOSE'].shift())
        self.candles['tr'] = self.candles[['tr0', 'tr1', 'tr2']].max(axis=1)

        self.candles['long_atr'] = self.candles['tr'].ewm(alpha=1 / self.params['long_atr_period'], adjust=False).mean()
        self.candles['short_atr'] = self.candles['tr'].ewm(alpha=1 / self.params['short_atr_period'], adjust=False).mean()

        self.candles = self.candles.drop(columns=['tr0', 'tr1', 'tr2', 'tr'])

    def strategy(self):
        if self.candles:
            self.get_candle(self.ticker)
        else:
            end_date = datetime.datetime.now()
            end_date = datetime.datetime(end_date.year, end_date.month, end_date.day, end_date.hour, end_date.minute, 0)

            time_delta = datetime.timedelta(minutes=25 * self.params['time_frame'])

            start_date = end_date - time_delta

            self.get_candles(self.ticker, start_date, end_date)

        candle_high_price = self.candles['HIGH'].iloc[-1]
        candle_low_price = self.candles['LOW'].iloc[-1]

        self.get_atr()
        high_prices = self.candles['HIGH'].values.tolist()
        low_prices = self.candles['LOW'].values.tolist()

        prev_sell_price = self.sell_price
        prev_buy_price = self.buy_price
        prev_cover_price = self.cover_price
        prev_short_price = self.short_price

        self.buy_price = max(high_prices[:-self.params['long_high_period']])
        self.sell_price = min(low_prices[:-self.params['long_low_period']])

        self.short_price = max(high_prices[:-self.params['short_high_period']])
        self.cover_price = min(low_prices[:-self.params['short_low_period']])

        long_stop_price = 0
        short_stop_price = 0

        long_atr = self.candles['long_atr'].iloc[-1]
        short_atr = self.candles['short_atr'].iloc[-1]

        if self.long_pos:
            long_stop_price = self.long_entry_price - self.params['long_stop_param'] * long_atr
            if long_stop_price > self.sell_price:
                self.sell_price = long_stop_price

        if self.short_price:
            short_stop_price = self.short_entry_price + self.params['short_stop_param'] * short_atr

            if short_stop_price < self.cover_price:
                self.cover_price = short_stop_price

        result = ''
        # positions open and close
        if self.long_pos:
            # close at stop (sell_price)
            if candle_low_price <= prev_sell_price:
                result += f'long position closed: {prev_sell_price}\n'
                self.long_pos = False
            else:
                result += f'long position price to close: {self.sell_price}\n'
        else:
            # buy if greater (buy_price)
            if candle_high_price >= prev_buy_price:
                result += f'long position opened: {prev_buy_price}\n'
                self.long_pos = True
            else:
                result += f'long position to open: {self.buy_price}\n'

        if self.short_pos:
            # close at stop (cover_price)
            if candle_high_price >= prev_cover_price:
                result += f'short position closed: {prev_cover_price}\n'
                self.short_pos = False
            else:
                result += f'short position to close: {self.cover_price}\n'
        else:
            # sell if less (short_price)
            if candle_low_price <= prev_short_price:
                result += f'short position opened: {prev_short_price}\n'
                self.short_pos = True
            else:
                result += f'long position to open: {self.short_price}\n'

        return self.sell_price, self.buy_price, self.cover_price, self.short_price
