import quandl

csv_name = input('What should the csv be called? ')

data = quandl.get("LBMA/GOLD", authtoken="Pa5fcY5AMKGfoipiGqjs", start_date="2017-02-25")

data = data.iloc[::-1]

data.to_csv('quandl_gold_data_{}.csv'.format(csv_name), mode = 'w+')

#End
