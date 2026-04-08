from backtesting import Strategy
from backtesting.lib import crossover
import talib as ta
import numpy as np

class RsiCross(Strategy):
    ns = 14
    nl = 28

    def init(self):
        self.rsiS, self.rsiL = self.I(self.calc_rsi_pair, self.data.Close, self.ns, self.nl)

    def calc_rsi_pair(self, close, n1, n2):
        rsiS = ta.RSI(close, timeperiod=n1)
        rsiL = ta.RSI(close, timeperiod=n2)
        return np.column_stack([rsiS, rsiL])

    def next(self):
        if crossover(self.rsiS, self.rsiL) and not self.position:
            self.buy()
        elif crossover(self.rsiL, self.rsiS):
            self.position.close()
        