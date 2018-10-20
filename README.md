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

![Price_Graph](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/price_graph.png)


This is .a dynamic Plotly graph and can be accessed in the Presentation notebook.

![Price_Graph](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/price_graph.gif)

### Feature Engineering on Price

I engineered out almost all of these features in favor of a spread (high-low), volume, and lagged change (n-hour change) to gauge volitility and momentum of price change. I used the function below to allow me to easily select which hour lags I wanted to use on the model. 

```python
# Lagging data function

def hour_change(shift, dataframe, shift_on):
    shift_column_name = '{}-hour-{}-shift'.format(shift, shift_on)
    change_column_name = '{}-hour-{}-change'.format(shift, shift_on)

    dataframe[shift_column_name] = np.nan
    dataframe[shift_column_name] = dataframe[shift_on].shift(shift)

    dataframe.fillna(method='bfill', inplace=True)

    dataframe[change_column_name] = dataframe[shift_on] - dataframe[shift_column_name]
    dataframe.drop(columns=[shift_column_name], inplace=True)

    return dataframe

# Function in action

shifts = [1, 2, 3, 4, 6, 8, 10, 12]
for x in shifts:
    eth_data = hour_change(x, eth_price_data, 'close')
```

### Google Trends Data

I chose this data because: 

* It's tracked on a 24/7 hourly basis 
* It can be a proxy for 'news-worthy' events 
* It can be a gauge of public awareness / investor interest 

BUT: 

* There's a two week lag on Google Trends data, which presents a use-case challenge 
* and more features do not necessarily lead to improved accuracy

As you can see below, trends for closely related concepts - like ethereum and its ticker - trend together, but different patterns can be seen between different ideas. I wanted to explore what effect this information might have. 

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/google_trends_data.png)


## Regression Modeling

Regression methods seek to predict a continuous value, and this often makes them more challenging than their classification counterparts. Here, my regression models seek to predict the future price.

### FBProphet - Additive Modeling
Ultimately, while I had hourly data going back 18 months, my best model performances occured when I fed the model smaller ranges of data, likely because it was less swayed by past trends that no longer represented the state of the market. This is the reasoning by creating lookback 'windows'. 

My best FBProhpet models had a lookback between 2-4 weeks. The model here looks back just shy of three weeks and then makes predictions (with confidence intervals) hourly for the next 24 hours after the end of the data. You'll notice the confidence intervals widen swiftly, as the model becomes less certain.

In the below image, the black dots are actual price points, the blue line is the predicted price, and the blue shaded area is the 95% confidence interval. The model forecasts hourly and forecast 24 hours beyond the data it has. Beyond this point, the confidence interval balloons dramatically. 

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/fbp_forecast.png)

FBProphet also gives you the ability to break out components and easily visualize these components to see if there are certain patterns across the time series at a more granular level. 

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/fbp_components.png)


## Classification Modeling

### Machine Learning Methods

As opposed to regression, classification attempts to predict a discrete (categorical) value. The classication here is binary and looks to predict whether the price will rise or fall in the next hour. 

I suspect that the multicollinearity between many of these features is adding (bias) noise to the model. My educated guess is that because of this, the explicit regularization applied by the logistic regression model explains its outperforming other models. 

I built out a quick way of running a complete gridsearch on a classification model with just a few tweeks.

``` python

# Creating dict to hold data with and without trend data for streamlined testing

training_sets = {'train': [target_train, features_train, target_val, features_val],
                'train_with_trend' : [target_with_trends_train, features_with_trends_train,
                                      target_with_trends_val, features_with_trends_val]}

# Building function to gridsearch multiple datasets and return relevent results

def test_classifiers(data, grid):
    results_dict = {}

    for data_set, splits in data.items():
        grid.fit(splits[1], splits[0])
        results_dict[data_set + ' results'] = [grid.best_score_, grid.best_params_, grid.score(splits[1], splits[0]), grid.score(splits[3], splits[2])]

    return results_dict

# Creating and Running GridSearch on Random Forest Model

from sklearn.ensemble import RandomForestClassifier

rft_param_grid = {'randomforestclassifier__n_estimators': [250, 350, 450],
                'randomforestclassifier__max_depth': [2, 6, 10, 14, 18, 22]}

rft_pipe = make_pipeline(RandomForestClassifier())

rft_grid = GridSearchCV(rft_pipe, rft_param_grid, scoring = "accuracy")

rft_results = test_classifiers(training_sets, rft_grid)

rft_results
```

Results were pretty muted across models. This was, generally, what I anticipated. Below is the best accuracies for the various classification models I ran. 

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/ml_model_perform.png)

Part of the challenge going forward will be deciding which features to keep and which to drop, because my feature importances across models were not terribly informative, as you can see from the random forest feature importance visualization below. The features that were slightly more important than the others were the one hour prices for Ethereum and Bitcoin, which seems reasonable. 

![Image](https://github.com/mattymecks/ethereum-forecasting/blob/master/images/rf_feat_import.png)

These models would benefit from additional rounds of training using different selections of features. It's possible that the bitcoin data is adding more noise than information. Additionally, a few of the features seem slightly more important than others, so focusing on those features may prove helpful. 

## Next Steps & Future Work

One of the things this project brought home for me, asides from being a great opportunity to get comfortable with time series data and real-world production considerations, was that not all problems are readily answerable. Sometimes it takes many, many iterations to see any improvement, and even then some things simply don't have trends or don't have trends that we can fully realize yet. I believe that insight will serve me well. That being said, there are some additional steps I'd like to take to continue to improve the project.

### Feature Engineering & Data Manipulation

A lot of the work that remains to be done is working with the data itself. I'd likely building out daily and weekly datasets, and continue to test different groups of features and time frames on the models themselves. This includes potential omitted variable bias from general financial market changes, regulator decisions, news coverage, and public sentiment (which might be able to be gauged via twitter as well as Google Trends).

### Regression / Statistical Inference

I’m currently working on a Bayesian Ridge Regression model, which is a new model for me, so I’m taking my time to make sure I full understand how it operates.

After that will be the standard ARIMA for time-series data. I suspect it will outperform other models that I’ve built.

### Classification / Machine Learning

My Random Forest appears to be overfitting, but my other models do not, which is unexpected and warrants further exploration.

Additionally, my XGBoost tuning results appear very similar to my AdaBoost results and I want to verify that

### Deep Learning

Deep learning models are still in development for this project. Depending on how much time I have to devote to personal projects in the near future, these may take a few weeks to a few months to fully built out. I’d like to try an RNN (both with LSTM cells and GRU cells) and a 1D CNN, which has shown promising results recently for other researchers.

## Libraries & Data Sources

#### Quandl

While I ended up not using gold data or other financial indicators, Quandl deserves a shout-out, as its where I would have gotten this data. Quandl is a great site (https://www.quandl.com/) with a great selection of free (and premium) financial databases that are easy to access and use.

#### PyTrends

PyTrends is an excellent, easy to use, Python package that turns Google Trends into a much more readily accessible API. Installation / docs for PyTrends here: https://github.com/GeneralMills/pytrends

#### FBProphet

FBProphet is a powerful, simple, accurate forecasting tools that utilizes additive modeling and is freely available from: https://pypi.org/project/fbprophet/ 

## Acknowledgments & Resources
I'd like to thank Matthew Chen, Neha Narwal, and Mila Shultz from Stanford University. Their Predicting Price Changes in Ethereum that served as the inspiration for this project. Their report can be found here: http://cs229.stanford.edu/proj2017/final-reports/5244039.pdf



