import pandas as pd
path = "./trabajo4.csv"
df = pd.read_csv(path)
pd.set_option('display.max_columns', None)
print(df.head())
print(df.dtypes)
print(df.isna().sum())
print(df.describe())
print(df["country"].value_counts())
print(df[df['country'].isna()])