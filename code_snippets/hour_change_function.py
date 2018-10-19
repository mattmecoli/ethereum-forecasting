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
