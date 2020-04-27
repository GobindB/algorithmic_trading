import pandas as pd 
import numpy as np 

# exchange rate link:
# https://open.canada.ca/data/en/dataset/1bc25b1e-0e02-4a5e-afd7-7b96d6728aac

# https://towardsdatascience.com/data-science-in-algorithmic-trading-d21a46d1565d

# load csv file
url = "https://raw.githubusercontent.com/GobindB/algorithmic_trading/master/10100008.csv"

types = {'REF_DATE' : int, 'VALUE' :int}
# Lines with too many fields (e.g. a csv line with too many commas)
# will by default cause an exception to be raised
rates = pd.read_csv(url, error_bad_lines=False, dtype=types)

# dictionary key method not preffered to .get() method - medium article

# pick preffered columns
rates_cols=['REF_DATE', 'VALUE']

# selet only closing spot price for currency pair
rates=rates[rates['Type of currency']=='United States dollar, closing spot rate']

# use only required columns and fill all null values with 0
rates=[rates_cols].fillna(0)

# creates a common index with CSV data
rates.index = pd.to_datetime(rates['REF_DATE'])

rates.drop(['REF_DATE'], axis=1, inplace=True)

rates.rename(columns={'VALUE': 'USD_CAD'}, inplace=True)

# use most recent day rate if weekend or markets are closed
while rates[rates==0].count(axis=0)['USD_CAD']/len(rates.index) > 0:
	print("Shifting rates. Days with rate at 0 = %",rates[rates == 0].count(axis=0)['USD_CAD']/len(rates.index))
	rates['yesterday']= rates['USD_CAD'].shift(1)
	rates['USD_CAD']  = np.where(rates['USD_CAD']==0, rates['yesterday'], rates['USD_CAD'])

# verify we dont have days with rates at 0
print("Days with rate at 0 = %", rates[rates==0].count(axis=0)['USD_CAD']/len(rates.index))

rates.drop(['yesterday'], axis=1, inplace=True)

rates.plot()
rates.tail()