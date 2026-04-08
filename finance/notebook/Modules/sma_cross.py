from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

class SmaCross(Strategy):
    ns = 5
    nl = 25

    def init(self):
        # 短期移動平均
        self.smaS = self.I(SMA, self.data["Close"], self.ns)
        # 長期移動平均
        self.smaL = self.I(SMA, self.data["Close"], self.nl)

    def next(self):
        # smaS > smaL で買う
        if crossover(self.smaS, self.smaL):
            self.buy()
        # smaS < smaL で売る
        elif crossover(self.smaL, self.smaS):
            self.position.close()