import yfinance as yf
import pytz
from datetime import datetime, timezone

utc_dt = datetime.now(timezone.utc)

PST = pytz.timezone('US/Pacific')

print("{} PST".format(utc_dt.astimezone(PST)))

msft = yf.Ticker("MSFT")

# get stock info

stock_info = msft.info
print("name: " + stock_info["longName"])

# get historical market data
hist = msft.history(period="1d")

print("hist")
print(hist)
open_price = None
close_price = None

for index, row in hist.iterrows():
    open_price = row['Open']
    close_price = row['Close']

value_change = close_price - open_price
percent_change = (value_change/open_price) * 100

print("value_change: ", str('%.2f' % value_change))
print("percent_change: ", str('%.2f' % percent_change))






#"longName":"Microsoft Corporation",