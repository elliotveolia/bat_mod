import pandas as pd
from config import BatteryConfig

# Display all rows and columns
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

df = pd.read_csv('data/Grid Import.csv')

print(df)

capacity = BatteryConfig.capacity_mw


print(capacity)
