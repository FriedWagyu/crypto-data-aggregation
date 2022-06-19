from pycoingecko import CoinGeckoAPI
import time
from datetime import datetime as dt
import xlwings as xw

# cg API
'''
Get historical market data include
price, market cap, 24h volume 
cg.get_coin_market_chart_range_by_id(id='bitcoin', vs_currency='usd', from='', to='')
Get current data 
name, price, market...
cg.get_coin_by_id(id='', localization='false')
'''
cg = CoinGeckoAPI()

# time range for price feed
unix_time_gmt_end = str(int(time.mktime(dt.utcnow().date().timetuple())))
unix_time_gmt_start = str(int(unix_time_gmt_end) - (365 * 24 * 60 * 60))
time_gmt_start = dt.fromtimestamp(int(unix_time_gmt_start))
time_gmt_end = dt.fromtimestamp(int(unix_time_gmt_end))
print('START:', time_gmt_start, unix_time_gmt_start)
print('END:', time_gmt_end, unix_time_gmt_end)

# token data holder
dict_token_data = None
dict_hist_data = None

# read excel
wb = xw.Book("datasheet.xlsx")
sheet_main = wb.sheets["main"]
sheet_main_shape = sheet_main.used_range.shape

# loop start
for i in range(2, sheet_main_shape[0] + 1):
    # prepare sheet
    token_name = sheet_main.range((i, 1)).value
    print(token_name)
    try:
        wb.sheets.add(name=token_name, before=None, after="bitcoin")
    except ValueError:
        print("exists")
    sheet_token = wb.sheets[token_name]
    sheet_token.range("A1:H1").value = ["time",
                                        "price",
                                        "interday_return",
                                        "market_cap",
                                        "circulate_supply",
                                        "total_volume"
                                        ]
    # get both data
    dict_token_data = cg.get_coin_by_id(id=token_name)
    dict_hist_data = cg.get_coin_market_chart_range_by_id(id=token_name, vs_currency='usd', from_timestamp=unix_time_gmt_start, to_timestamp=unix_time_gmt_end)
    # add max supply to main
    sheet_main.range((i, 5)).value = [dict_token_data["market_data"]["max_supply"]]
    # fill token data to sheet
    sheet_token.range("A2").value = dict_hist_data["prices"]
    sheet_token.range("C2").value = dict_hist_data["market_caps"]
    sheet_token.range("E2").value = dict_hist_data["total_volumes"]
    # calculate additional data
    for j in range(3, 367):
        sheet_token.range('C' + str(j)).value = ['=B' + str(j) + '/B' + str(j-1) + "-1"]
    for k in range(2, 367):
        sheet_token.range('E' + str(k)).value = ['=D' + str(k) + '/B' + str(k)]
    sheet_token.range("C2").value = None
    # fill main sheet
    sheet_main.range(i, 2).value = ["=" + token_name + "!D366"]
    if sheet_main.range((i, 5)).value is None:
        print("no max supply")
    else:
        sheet_main.range(i, 3).value = ["=E" + str(i) + "*" + token_name + "!B366"]
    sheet_main.range(i, 4).value = ["=" + token_name + "!E366"]
    sheet_main.range((i, 6),(i, 14)).value = ["=MIN(" + token_name + "!B:B)/MAX(" + token_name + "!B:B)-1",
                                              "=MIN(" + token_name + "!D:D)/MAX(" + token_name + "!D:D)-1",
                                              "=" + token_name + "!E366/" + token_name + "!E2-1",
                                              "=CORREL(bitcoin!B:B," + token_name + "!B:B)",
                                              "=CORREL(bitcoin!F:F," + token_name + "!F:F)",
                                              "=STDEV.S(" + token_name + "!C3:C366)",
                                              "=SQRT(365)*K" + str(i),
                                              sheet_token.range("A2").value,
                                              sheet_token.range("A366").value]
