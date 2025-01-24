from tradingbot import strategy

#from lumibot.credentials import IS_BACKTESTING #might use later

from lumibot.traders import Trader # for live deployment
from lumibot.backtesting import YahooDataBacktesting #framework for backtesting
from datetime import datetime
from creds import IS_BACKTESTING

start_date=datetime(2020,1,1)
end_date=datetime(2023,12,31)
cash_at_risk=0.5



if __name__ == 'main':
      if IS_BACKTESTING== True: #if we're backetesting
        strategy.backtest(
        YahooDataBacktesting,
        start_date,
        end_date,
        parameters={"symbol":"SPY",  "cash_at_risk":cash_at_risk } )
      else: #live trade

        trader= Trader() #create variable to host our live trading object
        trader.add_strategy(strategy=strategy) #import our MLTrader strategy 
        trader.run_all() #runs the strategy live