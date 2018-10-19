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
