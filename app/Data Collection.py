import csv
import HTMLParser
import pandas
import Quandl
import requests
import re
import itertools

__author__ = 'Jake'

def get_us_stock_exchange_data(exchange):
    response = requests.get('http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=%s&render=download' % exchange)
    data = response.text
    decoded = HTMLParser.HTMLParser().unescape(data)
    reader = csv.reader(decoded.splitlines(), delimiter=',', dialect='excel')
    reader.next()
    mydict = dict((rows[0].strip(), rows[1:9]) for rows in reader)
    for k,v in mydict.iteritems():
        if 'M' in v[2]:
            cap = int(float(re.sub('\$|M', '', v[2]))*1000000)
            v[2] = cap
        elif 'B' in v[2]:
            cap = int(float(re.sub('\$|B', '', v[2]))*1000000000)
            v[2] = cap
    return mydict

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

exchanges = ['NASDAQ', 'NYSE', 'AMEX']

nasdaq_dict = get_us_stock_exchange_data(exchanges[0])
nyse_dict = get_us_stock_exchange_data(exchanges[1])

nasdaq_screened = market_cap_screen(nasdaq_dict)
nyse_screened = market_cap_screen(nyse_dict)

x, y = price_screen(nasdaq_dict, exchanges[0].upper())

nyse_stocks, nyse_errors = price_screen(nyse_dict, exchanges[1].upper())

with open("NYSE_Errors.csv", "wb") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(nyse_errors.keys())
    writer.writerows(zip(*nyse_errors.values()))