import robin_stocks as r
from Robin.config import usr, pswd


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
    # print(len(r.get_all_positions(info=None)))
    portfolio = []
    list = r.get_all_positions(info=None)
    # print("Ticker" + '  |  ' + "Quantity" + "  |  " + "Average Price" + '  |  ' + "Date Purchased")
    for entry in list:
        quantity = entry['quantity']
        if quantity == '0.00000000':
            continue
        instrument = entry['instrument']
        avg_price = entry['average_buy_price']
        date = entry['created_at'].split('T')[0]
        ticker = r.stocks.get_symbol_by_url(instrument)
        # print(entry)
        # print(ticker + '  |  ' + quantity + '  |  ' + avg_price + '  |  ' + date)
        portfolio.append([ticker, quantity, avg_price, date])
        # print('\n')
    return portfolio

def portfolio_to_txt():
    list = get_all_stocks()
    f = open('list.txt', 'w')
    for entry in list:
        f.write(str(entry))
        f.write('\n')
    f.close()



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


if __name__ == '__main__':
    main()
