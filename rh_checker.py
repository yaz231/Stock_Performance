from typing import List, Any, Union

import robin_stocks as r
import pandas as pd
import datetime as dt
from datetime import date
import pandas_datareader as web
from Robin.config import usr, pswd


earliest_date = ""
today = str(date.today())
year_today = int(today.split('-')[0])
month_today = int(today.split('-')[1])
day_today = int(today.split('-')[2])

def login():
    login = r.login(usr, pswd)

def get_shares(ticker):
    positions_data = r.get_open_stock_positions()
    for item in positions_data:
        item['symbol'] = r.get_symbol_by_url(item['instrument'])
        if item['symbol'] == ticker:
            print("{} shares of {}".format(item['quantity'], item['symbol']))

def get_portfolio():
    positions_data = r.get_open_stock_positions()
    with open('portfolio.txt', 'w') as f:
        for item in positions_data:
            item['symbol'] = r.get_symbol_by_url(item['instrument'])
            print("{} | {}".format(item['symbol'], item['average_buy_price']))
            f.write(item['symbol'] + '\n')

def get_Net():
    my_stocks = r.build_holdings()
    profits, losses = 0, 0
    for key, value in my_stocks.items():
        # print(key, value)
        change = float(value['equity_change'])
        # print(change)
        # print(float(change))
        # print(type(float(change)))
        print("{} | {}".format(key, change))
        if change > 0:
            profits += change
        else:
            losses += change
    print("Profits: " + str(profits))
    print("Losses: " + str(losses))

def quote_category():
    earnings = r.get_all_stocks_from_market_tag('most-popular-under-25')
    ###'biopharmaceutical', 'upcoming-earnings', 'most-popular-under-25', and 'technology'
    for stock in earnings:
        print("{} | {}".format(stock['symbol'], stock['last_trade_price']))
    # r.get_all_stocks_from_market_tag('technology')  # get all tech tags

def get_all_stocks():
    portfolio = pd.DataFrame(columns=['Ticker', 'Quantity', 'Average_Price', 'Date'])
    list = r.get_all_positions(info=None)
    for entry in list:
        quantity = entry['quantity']
        if quantity == '0.00000000':
            continue
        instrument = entry['instrument']
        avg_price = entry['average_buy_price']
        date = entry['created_at'].split('T')[0]
        ticker = r.stocks.get_symbol_by_url(instrument)
        portfolio = portfolio.append(pd.Series([ticker, quantity, avg_price, date], index=['Ticker', 'Quantity', 'Average_Price', 'Date']), ignore_index=True)
    portfolio = portfolio.set_index('Ticker')
    # portfolio = portfolio.set_index(pd.DatetimeIndex(portfolio['Ticker'].values))
    global earliest_date
    earliest_date = portfolio['Date'].min()
    return portfolio

def portfolio_to_txt():
    portfolio = get_all_stocks()
    f = open('portfolio.txt', 'w')
    # f.write("Ticker" + ' | ' + "Quantity" + " | " + "Average Price" + ' | ' + "Date Purchased")
    # f.write('\n')
    # for entry in list:
    #     f.write(str(entry))
    #     f.write('\n')
    vals = portfolio.values
    print(vals)
    f.write(vals)
    f.close()

def get_SP500(earliest_day):
    year = int(earliest_day.split('-')[0])
    month = int(earliest_day.split('-')[1])
    day = int(earliest_day.split('-')[2])
    start = dt.datetime(year, month, day)
    end = dt.datetime(year_today, month_today, day_today)
    df = web.DataReader('^GSPC', 'yahoo', start, end)
    df.to_csv('GSPC.csv')

def calculate_rate_return_SP500(date):
    df = pd.read_csv('GSPC.csv')
    df
    print(date)
    # print(df[date])
    # close = df[date]['Close']
    # close_today = df[today]['Close']
    # return close/close_today - 1

# def calculate_rate_return_SP500(ticker):


def main():
    login()

    # quote_category()
    # get_portfolio()
    # get_shares('NIO')
    # NIOData = [item for item in positions_data if item['symbol'] == 'NIO']
    # sellQuantity = float(NIOData['quantity'])//2.0
    # print(sellQuantity)
    # r.order_sell_limit('TSLA',sellQuantity,200.00)
    # profile = r.build_user_profile()
    # print(profile)
    # my_stocks = r.build_holdings()
    # for key, value in my_stocks.items():
    #     print(key, value)
    # get_Net()
    # print(r.get_all_positions(info=None))
    # print(get_all_stocks())
    portfolio_to_txt()
    # get_SP500(earliest_date)
    # with open('list.txt', 'r') as f:
    #     lines = f.readlines()[1:]
    #     for line in lines:
    #         print(line[3])
    #         rr = calculate_rate_return_SP500(line[3])
    #         print(line[0] + "Return of: " + rr)



if __name__ == '__main__':
    main()
