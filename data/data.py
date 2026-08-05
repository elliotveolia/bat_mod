import sys
import pandas as pd

df = pd.read_csv('Grid Import.xlsx - Grid Import.xls.csv')

# Convert to datetime
df['DateTime'] = pd.to_datetime(df['Date'], format='%d %b %Y %H:%M')

# Extract date and time
df['Date'] = df['DateTime'].dt.strftime('%d %b %Y')
df['Time'] = df['DateTime'].dt.strftime('%H:%M')

# Drop the temporary column
df = df.drop('DateTime', axis=1)

# Rename the long column to 'Load'
df = df.rename(columns={'Total Grid Power to Site (Calc) (kWHr)': 'Load'})

# Keep only the columns you want
df = df[['Day', 'Date', 'Time', 'Load']]

# Convert to datetime
df['Date'] = pd.to_datetime(df['Date'], format='%d %b %Y')

# Filter for 2024
df = df[df['Date'].dt.year == 2024]

# Save final data product
df.to_csv('Grid Import.csv', index=False)
