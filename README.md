This program uses lumibot, an algorithmic trading bot library, to connect to the alpaca brokerage using an API key in order to send a buy/sell order to a specific stock. 

This algorithmic bot uses a pre trained ML model that will trade on News headlines from three days prior to when a trade will be fufilled. The model returns a sentiment of either "Positive", "Negative", or "Neutral", based off headlines. It also returns a probability value. If the sentiment is positive and the probability is greater than 0.999, then the bot will buy the stock. If sentiment is negative and the probability value is greater than 0.999, then it will automatically sell the stock. Quantity and cash at risk can also be modified manually.

Backtesting was conducted on the SPY stock, an ETF trust that tracks the performance of the S&P 500.

Backtesting Statisics Summary on the SPY

3 year period (2021-2023): 216%
