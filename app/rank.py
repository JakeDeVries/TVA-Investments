from bs4 import BeautifulSoup
import csv
import requests

def finviz_metrics(ticker):
    stock_metrics = {}
    stock_metrics[ticker] = {}
    response = requests.get('http://finviz.com/quote.ashx?t=%s' % ticker)
    soup = BeautifulSoup(response.text)
    table = soup.find('table', class_ = 'snapshot-table2')
    data = table.find_all('td')
    for i in range(len(data)):
        if i % 2 == 0:
            metric = data[i].text.encode("utf-8")
            value = data[i+1].text.encode("utf-8")
        elif i % 2 == 1:
            pass
        stock_metrics[ticker][metric] = value
    return stock_metrics