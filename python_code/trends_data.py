# more info on pytrends here: https://github.com/GeneralMills/pytrends

from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

kw_list = input('Enter comma-separated, list-formated, string-formated values: ')
if len(kw_list) < 1: kw_list = ['btc', 'crypto', 'cryptocurrency']
# ['Ethereum', 'eth', 'bitcoin', 'blockchain', 'buy ethereum']

csv_name = input('What should the csv be called? ')

# Usage note: it'll only return 'weeks' or hourly data. So if you tried to grab six days, it wouldn't return anything and if you tried to grab eight days, it'll only return seven.

#returns pandas dataframe, so can treat it as such

#not hardcoded, project specific. Could turn these into inputs

df = pytrends.get_historical_interest(kw_list,
                                         year_start=2017, month_start=2, day_start=20, hour_start=0,
                                         year_end=2018, month_end=9, day_end=8, hour_end=0,
                                         cat=0, geo='', gprop='', sleep=4)

# always be aware of rate limits, normally I'd put this in a loop and have it time.sleep() but this function happens to have a handy-dandy built-in 'sleep'

# as always, caution, as this will overwrite existing csv of the same name

df.to_csv('google_trends_data_{}.csv'.format(csv_name), mode = 'w+')


# End
