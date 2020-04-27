import pandas as pd
import matplotlib.pyplot as plt

dataset = "https://media.githubusercontent.com/media/GobindB/algorithmic_trading/master/18100030.csv"
df_cols = ['REF_DATE', 'North American Product Classification System (NAPCS)', 'VALUE']

df = pd.read_csv(dataset, error_bad_lines=False, usecols=df_cols)

categories = list(df[list(df)[1]].drop_duplicates())

# Prepare an empty dataframe to fill with properly indexed economic data
new_df = pd.DataFrame(columns=df_cols)

# creates a common index with CSV data
df.index = pd.to_datetime(df['REF_DATE'])
new_df.index = pd.to_datetime(new_df['REF_DATE'])

df.drop(['REF_DATE'], axis=1, inplace=True)
new_df.drop(['REF_DATE'], axis=1, inplace=True)

# Loop through the economic indicators and put each one in a dedicated column
for cat in categories:
    # Data can have problems, and not all indicators will make it through
    try:
        new_df[cat] = df[df[list(df)[0]] == cat]['VALUE']
    except Exception as e:
        print("failed on", cat, e)

print(new_df)

# new_df.plot()
# plt.show()
