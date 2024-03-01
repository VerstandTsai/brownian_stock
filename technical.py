import matplotlib.pyplot as plt
import numpy as np

class Strategy:
    def __init__(self):
        self.cash = 0
        self.stocks = 0
        self.test_record = {}
        self.verbose = True

    def _buy(self, price, amount, day):
        if amount <= 0 or self.cash < price * amount:
            return
        self.cash -= price * amount
        self.stocks += amount
        if self.verbose:
            print(f'Bought\t{amount:>8} at {price:>8.2f} on day {day:>4}')

    def _sell(self, price, amount, day):
        if amount <= 0 or self.stocks < amount:
            return
        self.cash += price * amount
        self.stocks -= amount
        if self.verbose:
            print(f'Sold\t{amount:>8} at {price:>8.2f} on day {day:>4}')

    def test(self, prices, fund, verbose=True):
        '''
        The user has to define their strategy here by overriding
        '''

class MovingAverage(Strategy):
    def __init__(self, ma_length):
        super().__init__()
        self.ma_length = ma_length

    def test(self, prices, fund, verbose=True):
        self.verbose = verbose

        self.cash = fund
        self.stocks = 0
        ma = moving_average(prices, self.ma_length)

        was_below = prices[self.ma_length] < ma[0]
        for i in range(self.ma_length, prices.size):
            ma_index = i - self.ma_length

            if prices[i] > ma[ma_index] and was_below:
                self._buy(prices[i], self.cash // prices[i], i+1)
            if prices[i] < ma[ma_index] and not was_below:
                self._sell(prices[i], self.stocks, i+1)

            was_below = prices[i] < ma[ma_index]

        self._sell(prices[-1], self.stocks, prices.size)
        self.test_record['profit'] = self.cash - fund
        self.test_record['return_rate'] = self.test_record['profit'] / fund
        if verbose:
            print(f'Cash remaining:\t{self.cash:>16.2f}')
            print(f'Net profit:\t{self.test_record["profit"]:>16}')
            print(f'Rate of return:\t{self.test_record["return_rate"]:>16.2%}')

def gen_prices(num_days=240, init_price=100, volatility=0.01):
    '''
    Simulates stock prices with geometric Brownian motion
    '''
    return init_price * np.exp(np.cumsum(volatility * np.random.randn(num_days))) // 0.01 / 100

def moving_average(prices, length=20):
    '''
    Calculates the moving average of the stock prices within a given time frame
    '''
    ma = np.zeros(prices.size - length)
    for i in range(prices.size - length):
        ma[i] = np.mean(prices[i : i+length])
    return ma

if __name__ == '__main__':
    ma_length = 20
    strat = MovingAverage(ma_length)
    batch_size = 1000
    return_rates = np.zeros(batch_size)
    for i in range(batch_size):
        prices = gen_prices(240, 100)
        ma = moving_average(prices, ma_length)
        strat.test(prices, 1000000, False)
        return_rates[i] = strat.test_record['return_rate']
    print(f'{return_rates.mean():.2%}')
    plt.hist(return_rates, bins=20)
    plt.show()
    #plt.plot(prices)
    #plt.plot(np.arange(ma_length, prices.size), ma)
    #plt.show()

