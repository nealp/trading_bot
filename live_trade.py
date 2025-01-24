from tradingbot import MLTrader, strategy, API_KEY,API_SECRET,BASE_URL
from lumibot.credentials import IS_BACKTESTING
from lumibot.traders import Trader # for  live deployment


if __name__ == 'main':
      trader= Trader() #create variable to host our live trading object
      trader.add_strategy(MLTrader) #import our MLTrader strategy 
      trader.run_all() #runs the strategy live 