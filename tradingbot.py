from lumibot.brokers import Alpaca #broker
from lumibot.backtesting import YahooDataBacktesting #framework for backtesting
from lumibot.strategies.strategy import Strategy #tradingbot
from lumibot.traders import Trader # for deployment

from datetime import datetime #time
from alpaca_trade_api import REST 

from alpaca_trade_api import REST #dynamically get things from alpaca
from timedelta import Timedelta #for calculating time diff.

from finbert_utils import estimate_sentiment #ML model

import creds
from creds import IS_BACKTESTING

API_KEY = creds.API_KEY
API_SECRET= creds.API_SECRET
BASE_URL= creds.BASE_URL

#pass this to ALPACA API
ALPACA_CREDS = {

    "API_KEY" :API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER" : True    #we are paper trading
}


#can modift stop loss and take profit here
take_profit_percent= 1.20
stop_loss_percent=0.95


class MLTrader(Strategy):
#this method will run once when bot starts
    def initialize(self,symbol:str="SPY", cash_at_risk:float=0.5):
        self.symbol=symbol
        self.sleeptime = "24H"
        self.last_trade= None
        self.cash_at_risk= cash_at_risk #cash at risk can be tweaked if we want to make bigger or smaller trades 
#creating instance of our API with base URL and API key and secret
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET) 

    #for position and cash management
    #lets us choose how much shares of a position we want rel to our cash
    def position_sizing(self): 

        cash = self.get_cash() #get the current cash val in account
        last_price= self.get_last_price(self.symbol) #returns last known price of asset
        quantity= (cash *self.cash_at_risk // last_price) #Formula that determines how many of asset we'll trade per order
        return cash, last_price, quantity
    
    def get_dates(self):

        today = self.get_datetime() #todays date
        three_days_prior = today - Timedelta(days=3) #three days before

        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

#gets news from three days prior
    def get_sentiment(self):
        today,three_days_prior= self.get_dates()
        news= self.api.get_news(symbol=self.symbol,
                                start=three_days_prior,
                                end=today)
        news= [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news) #our ML model takes in news headlines as input layer and returns p (0-1) and positive/negative/neutral sentiment
        #note: only trade on positive/negative sentiment
        return probability , sentiment #returns news headlines

    #will run on every tick 
    #trading loop
    def on_trading_iteration(self):
        cash, last_price, quantity= self.position_sizing()  #from our method
        probability, sentiment = self.get_sentiment() #gives probability and sentiment for ML model

        #creates order
#will only create order if we have more cash than the last price of the stock
        if cash> last_price:
#if sentiment is strong positive            
            if sentiment == "positive" and probability > 0.999:
                if self.last_trade == "sell": #sells all stocks if last order as a sell to be safe
                    self.sell_all()

                order = self.create_order(
                    self.symbol,
                    quantity,
                    "buy",
                    type="bracket",
                    take_profit_price=last_price*take_profit_percent ,#take profit at 20%
                    stop_loss_price=last_price*stop_loss_percent #stop loss of 5%
                )
                #submit order to alpaca
                self.submit_order(order)
                self.last_trade="buy"
#if sentiment is strong negative
            elif sentiment == "negative" and probability > 0.999:
                if self.last_trade == "buy":  #sells all the assets if the last order was a buy order
                    self.sell_all()

                order = self.create_order(
                        self.symbol,
                        quantity,
                        "sell",
                        type="bracket",
                        take_profit_price= last_price*(take_profit_percent-(2*(take_profit_percent-1))) ,#take profit at 20%
                        stop_loss_price= last_price*(stop_loss_percent-(2*(stop_loss_percent-1))) #stop loss of 5%
                        )
                            #submit order to alpaca
                self.submit_order(order)
                self.last_trade="sell"
    def after_market_closes(self):
            self.log_message("The market is closed")
            self.log_message(f"The total value of our portfolio is {self.portfolio_value}")
            self.log_message(f"The amount of cash we have is {self.cash}")


#strt and end dates **IMPORTANT**

#can tweak these
start_date=datetime(2020,1,1)
end_date=datetime(2023,12,31)
cash_at_risk=0.5

#our broker is Alpaca
broker = Alpaca(ALPACA_CREDS)

#instance of of our tradingbot
#stock currently being traded is SPY
#cash at risk determines size of trade. (0-1) 
strategy = MLTrader(name='mlstrat',broker=broker,parameters={"symbol":"SPY" , 
                                                             "cash_at_risk":cash_at_risk}) #**


if IS_BACKTESTING: #if we're backetesting
    MLTrader.backtest(
    YahooDataBacktesting,
    start_date,
    end_date,
    parameters={"symbol":"SPY",  "cash_at_risk":cash_at_risk } )
else: #live trade

    trader= Trader() #create variable to host our live trading object
    trader.add_strategy(strategy) #import our MLTrader strategy 
    trader.run_all() #runs the strategy live




#sidie notes 

#set up env vars