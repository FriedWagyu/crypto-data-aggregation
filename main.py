from pycoingecko import CoinGeckoAPI
import json
import time
from datetime import datetime as dt


cg = CoinGeckoAPI()

# time range for price feed
unix_time_gmt_end = time.mktime(dt.utcnow().date().timetuple())
unix_time_gmt_start = unix_time_gmt_end - (365 * 24 * 60 * 60)
time_gmt_start = dt.fromtimestamp(unix_time_gmt_start)
time_gmt_end = dt.fromtimestamp(unix_time_gmt_end)
print('START:', time_gmt_start)
print('END:', time_gmt_end)

# token data holder
'''
Get historical market data include
price, market cap, 24h volume 
cg.get_coin_market_chart_range_by_id(
id='bitcoin', vs_currency='usd', from='', to='')
'''
'''
Get current data 
name, price, market...
cg.get_coin_by_id(id='', localization='false')
'''
dict_data = None











#cg.get_coin_market_chart_range_by_id()

