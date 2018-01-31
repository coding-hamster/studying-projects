import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

srz6 = pd.read_csv('SRU6 [Price]5minute.txt')


srz6['Date'] = pd.to_datetime(srz6['DATE'].astype(str), format='%Y%m%d')
srz6['Time'] = pd.to_datetime(srz6['TIME'].astype(str), format='%H%M%S')

def combine_date_time(df, datecol, timecol):
    return df.apply(lambda row: row[datecol].replace(
                                hour=row[timecol].hour,
                                minute=row[timecol].minute),
                    axis=1)
def rolling_mean(series, window):
    return np.round(pd.rolling_mean(series, window=window), 2)
def regular_plot(series, title):
    srz6[series].plot(grid=True, figsize=(8, 5), title=title)


srz6['Datetime'] = combine_date_time(srz6, 'Date', 'Time')
srz6.index = srz6['Datetime']

srz6['42d'] = rolling_mean(srz6['CLOSE'], 42)
srz6['252d'] = rolling_mean(srz6['CLOSE'], 252)

srz6['42-252'] = srz6['42d'] - srz6['252d']
srz6['42-252'].head()

SD = 50
srz6['Regime'] = np.where(srz6['42-252'] > SD, 1, 0)
srz6['Regime'] = np.where(srz6['42-252'] < -SD, -1, srz6['Regime'])
srz6['Regime'].value_counts()

close_plot = regular_plot('CLOSE',"Future's price")
plt.show(close_plot)

rolling_means_plot = srz6[['CLOSE', '42d', '252d']].plot(grid=True, figsize=(8, 5), title='Rolling means 42 and 252 steps')
plt.show(rolling_means_plot)

