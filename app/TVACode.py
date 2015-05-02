
# coding: utf-8

# In[37]:

from bs4 import BeautifulSoup
import csv
import os
import requests

os.chdir('/Users/Jack/Desktop/')
nasdaq_reader = csv.reader(open('NASDAQ_Stocks.csv', 'rU'), delimiter = ',', dialect = 'excel')
# nasdaq_stocks = dict((rows[0],rows[6]) for rows in nasdaq_reader)

row = 0
count = 1414
a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []

for rows in nasdaq_reader:
    if (row == 0):
        a+=(rows[:1414])
    elif (row == 1):
        b+=(rows[:1414])
    elif (row == 2):
        c+=(rows[:1414])
    elif (row == 3):
        d+=(rows[:1414])
    elif (row == 4):
        e+=(rows[:1414])
    elif (row == 5):
        f+=(rows[:1414])
    elif (row == 6):
        g+=(rows[:1414])
    elif (row == 7):
        h+=(rows[:1414])
    
    row+=1

nasdaq_stocks = dict(zip(a, f))
print nasdaq_stocks


        


# In[ ]:

basic_industries = []
capital_goods = []
consumer_durables = []
consumer_non_durables = []
consumer_services = []
energy = []
finance = []
healthcare = []
miscellaneous = []
n_a = []
public_utilities = []
technology = []
transportation = []


for key in nasdaq_stocks:
    if nasdaq_stocks[key] == 'Consumer Services':
        consumer_services.append(key)
    elif nasdaq_stocks[key] == 'Technology':
        technology.append(key)
    elif nasdaq_stocks[key] =='Transportation':
        transportation.append(key)
    elif nasdaq_stocks[key] =='Finance':
        finance.append(key)
    elif nasdaq_stocks[key] == 'Basic Industries':
        basic_industries.append(key)
    elif nasdaq_stocks[key] == 'Health Care':
        healthcare.append(key)
    elif nasdaq_stocks[key] == 'Miscellaneous':
        miscellaneous.append(key)
    elif nasdaq_stocks[key] == 'Consumer Non-Durables':
        consumer_non_durables.append(key)
    elif nasdaq_stocks[key] == 'Public Utilities':
        public_utilities.append(key)
    elif nasdaq_stocks[key] == 'Consumer Durables':
        consumer_durables.append(key)
    elif nasdaq_stocks[key] == 'n/a':
        n_a.append(key)
    elif nasdaq_stocks[key] == 'Capital Goods':
        capital_goods.append(key)
    elif nasdaq_stocks[key] == 'Energy':
        energy.append(key)

        
        
# In[47]:

def finviz_metrics(ticker):
    stock_metrics = {}
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
        stock_metrics[metric] = value
    return stock_metrics


# In[48]:

def stock_data(stocks):
    mydict = {}
    for stock in stocks:
        try:
            stock_metrics = finviz_metrics(stock)
            forward_pe = stock_metrics['Forward P/E']
            peg = stock_metrics['PEG']
            p_fcf = stock_metrics['P/FCF']
            debt_eq = stock_metrics['Debt/Eq']
            eps_this_y = stock_metrics['EPS this Y']
            eps_next_y = stock_metrics['EPS next Y']
            eps_next_five_y = stock_metrics['EPS past 5Y']
            roa = stock_metrics['ROA']
            roe = stock_metrics['ROE']
            roi = stock_metrics['ROI']
            operating_margin = stock_metrics['Oper. Margin']
            beta = stock_metrics['Beta']
            mydict[stock] = [forward_pe, peg, p_fcf, debt_eq, eps_this_y,
                            eps_next_y, eps_next_five_y, roa, roe,
                            roi, operating_margin, beta]
        except AttributeError:
            pass
    return mydict


# In[49]:

final_basic = stock_data(basic_industries)
final_capital = stock_data(capital_goods)
final_durables = stock_data(consumer_durables)
final_non_durabes = stock_data(consumer_non_durables)
final_services = stock_data(consumer_services)
final_energy = stock_data(energy)
final_finance = stock_data(finance)
final_healthcare = stock_data(healthcare)
final_miscellaneous = stock_data(miscellaneous)
final_n_a = stock_data(n_a)
final_public_utilities = stock_data(public_utilities)
final_technology = stock_data(technology)
final_transportation = stock_data(transportation)


# In[50]:




# In[22]:




# In[ ]:

with open("Basic_Industries.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_basic.keys())
   writer.writerows(zip(*final_basic.values()))

with open("Capital_Goods.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_capital.keys())
   writer.writerows(zip(*final_capital.values()))

with open("Consumer_Durables.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_durables.keys())
   writer.writerows(zip(*final_durables.values()))
    
with open("Consumer_Non_Durables.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_non_durabes.keys())
   writer.writerows(zip(*final_non_durabes.values()))
    
with open("Consumer_Services.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_services.keys())
   writer.writerows(zip(*final_services.values()))
    
with open("Energy.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_energy.keys())
   writer.writerows(zip(*final_energy.values()))
    
with open("Finance.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_finance.keys())
   writer.writerows(zip(*final_finance.values()))

with open("Healthcare.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_healthcare.keys())
   writer.writerows(zip(*final_healthcare.values()))

with open("Miscellaneous.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_miscellaneous.keys())
   writer.writerows(zip(*final_miscellaneous.values()))

with open("N_A.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_n_a.keys())
   writer.writerows(zip(*final_n_a.values()))

with open("Public Utilities.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_public_utilities.keys())
   writer.writerows(zip(*final_public_utilities.values()))
    
with open("Technology.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_technology.keys())
   writer.writerows(zip(*final_technology.values()))

with open("Transportation.csv", "wb") as outfile:
   writer = csv.writer(outfile)
   writer.writerow(final_transportation.keys())
   writer.writerows(zip(*final_transportation.values()))

