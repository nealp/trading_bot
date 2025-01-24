from tradingbot import MLTrader, strategy
from lumibot.credentials import IS_BACKTESTING #might use later
from lumibot.traders import Trader # for live deployment


if __name__ == 'main':
      trader= Trader() #create variable to host our live trading object
      trader.add_strategy(strategy=strategy) #import our MLTrader strategy 
      trader.run_all() #runs the strategy live 