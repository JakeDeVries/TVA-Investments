
__author__ = 'Jake'

import csv
import HTMLParser
import pandas
import Quandl
import requests

exchanges = ['NASDAQ', 'NYSE', 'AMEX']


def get_us_stock_exchange_data(exchange):
    response = requests.get('http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download' % exchange)
    data = response.text
    decoded = HTMLParser.HTMLParser().unescape(data)
    reader = csv.reader(decoded.splitlines(), delimiter=',', dialect='excel')
    reader.next()
    return dict((rows[0].strip(), rows[1:9]) for rows in reader)

nasdaq_dict = get_us_stock_exchange_data(exchanges[0])
nyse_dict = get_us_stock_exchange_data(exchanges[1])

def market_cap_screen(dictionary):
    screened = {}
    minimum_cap = 2000000000
    for key in dictionary:
        try:
            market_cap = float(dictionary[key][2])
            if market_cap >= minimum_cap:
                screened[key] = dictionary[key][0:9]
        except ValueError:
            pass
    return screened

nasdaq_screened = market_cap_screen(nasdaq_dict)
nyse_screened = market_cap_screen(nyse_dict)

def price_screen(dictionary, exchange):
    screened = {}
    errors = {}
    for key in dictionary:
        try:
            price = dictionary[key][1]
            if price != 'n/a':
                price = float(price)
                df = Quandl.get('GOOG/%s_%s' % (exchange, key), authtoken='FLmPR53xNVmgbJqhVrz7')
                rolling_means = pandas.rolling_mean(df['Close'], 200)
                moving_average_today = rolling_means.iloc[-1]
                if price >= moving_average_today:
                    screened[key] = dictionary[key][0:9]
            else:
                pass
        except (Quandl.Quandl.DatasetNotFound, Quandl.Quandl.ErrorDownloading):
            errors[key] = dictionary[key][0:9]
    return screened, errors

x, y = price_screen(nasdaq_dict, exchanges[0].upper())

nyse_stocks, nyse_errors = price_screen(nyse_dict, exchanges[1].upper())

with open("NYSE_Errors.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(nyse_errors.keys())
   writer.writerows(zip(*nyse_errors.values()))


