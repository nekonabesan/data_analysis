from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import numpy as np

class MacdCross(Strategy):
    n1 = 12
    n2 = 26
    n3 = 9

    def init(self):
        self.macd, self.macdsignal = self.I(self.MACD, self.data.Close, self.n1, self.n2, self.n3)

    def MACD(self, close, n1, n2, n3):
        macd, macdsignal, _ = ta.MACD(close, fastperiod=n1, slowperiod=n2, signalperiod=n3)
        return np.column_stack([macd, macdsignal])

    def next(self):
        if crossover(self.macd, self.macdsignal) and not self.position:
            self.buy()
        elif crossover(self.macdsignal, self.macd):
            self.position.close()