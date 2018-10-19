# Ethereum Forecasting

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/ethereum.png)

### Project Overview 

This is still an ongoing project, so some parts are unfinished or unpolished, and will become increasingly finished and polished as I push updates. 

This focus of this project to build forecasting models for Ethereum, both on:<br><br>
    1) price using various regression and time series analysis models, and <br>
    2) whether price would rise or fall in the next hour using machine learning model (and eventually neural nets).  

Regression, classification, and neural net models are still being built out.

The influence of the use case on the ultimate design here is one of my favorite parts of this project. While working with time-series data is a welcome challenge and the feature engineering is intriguing, the most interesting part has been building something with a specific ‘customer’ in mind. For this project, I'm working with a friend who does some casual day trading with cryptocurrencies. I had to build models that were readable and useable for him, and the data had to be readily available.  <br>

For example, the trends data was mostly used to see if information about how searched something was had any informative value for the model. <br>

But, there’s a two week delay on Google Trends data, so this information isn’t useful in a production setting. But if trend data like that had informative value for the model, there are certain proxies or estimators  available that I would explore with my friend. <br>

Having to think through problems like this gives me a better sense of how these models have to operate in production and makes me a better data scientist.  

### Data Import

``` python 

import time
import requests
import pandas as pd

#Intializing the database

url = 'https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24'
initial_response = requests.post(url)
initial_data = initial_response.json()['Data']
initial_data.reverse()
master_df = pd.DataFrame(initial_data)
master_df = master_df.set_index('time')

start_time_count = int(master_df.index[0])
end_time_count = 1488067199
round_count = 0
# 1488067200 in the unix time for Februrary 26, 2017 at 12am UTC
# This will form our data endpoint

while start_time_count > end_time_count:

    url_temp = url = 'https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24&toTs={}'.format(start_time_count)

    temp_response = requests.post(url_temp)
    temp_data = temp_response.json()['Data']
    temp_data.reverse()
    temp_df = pd.DataFrame(temp_data)
    temp_df = temp_df.set_index('time')

    master_df = master_df.append(temp_df)
    start_time_count -= 86400
    round_count += 1
    if round_count%500 is True:
        print(round_count)
        time.sleep(5)
        continue
    else:
        time.sleep(5)
        continue
    # always be careful about rate limits. The limit is closer to 3 seconds, but doesn't hurt to be safe when you can afford to be

# writing the mostly un-touched data to csv for later ETL

master_df.to_csv('eth_hourly_data.csv', mode = 'w+')

#End
```

## Datasets & Features
 
Cryptocurrencies trade 24/7, unlike most other financial instruments, so the data is an uninterrupted look at the past 18 months of Ethereum prices. <br>

One of the challenges of cryptocurrency data is that it can be difficult to tie it to more standard market indicators (commodity prices like gold or oil or market averages like stock indexes or bond yields) because of its 24/7 trading nature. Given more time, I would likely engineer a daily and/or weekly dataset and then interpolate missing dates (weekends and holidays) for these more traditional market indicators. I began but did not get to finish that process, and the amount of what is essentially educated guesswork for night and weekend hours required to bring something like gold price down to an hourly level presented problems of data fidelity. <br>

I primarily used hourly data pulled from the CryptoCompare on Ethereum and Bitcoin prices. 




