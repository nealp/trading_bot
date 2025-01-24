from tradingbot import MLTrader, strategy, API_KEY,API_SECRET,BASE_URL
from lumibot.credentials import IS_BACKTESTING
from lumibot.traders import Trader # for  live deployment


if __name__ == 'main':
      trader= Trader()
      trader.add_strategy(MLTrader)
      trader.run_all()
      trader.stop_all()
       