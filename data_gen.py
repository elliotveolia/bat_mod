import pandas as pd
from pathlib import Path


INPUT_FILE = Path("data/Grid Import.xlsx - Grid Import.xls.csv")
OUTPUT_FILE = Path("data/Grid Import.csv")


# Read the original input file
df = pd.read_csv(INPUT_FILE)


# Convert the original timestamp column
df["DateTime"] = pd.to_datetime(
    df["Date"],
    format="%d %b %Y %H:%M",
    errors="coerce"
)


# Remove rows with invalid timestamps
df = df.dropna(subset=["DateTime"]).copy()


# Keep only data from 2024
df = df[df["DateTime"].dt.year == 2024].copy()


# Rename the long energy column to a consistent name
df = df.rename(
    columns={
        "Total Grid Power to Site (Calc) (kWHr)": "load_kwh"
    }
)


# Confirm that the expected energy column exists
if "load_kwh" not in df.columns:
    raise KeyError(
        "Could not find the energy column. Available columns are: "
        f"{list(df.columns)}"
    )


# Convert energy values to numeric
df["load_kwh"] = pd.to_numeric(df["load_kwh"], errors="coerce")
df = df.dropna(subset=["load_kwh"]).copy()


# Recreate date and time columns from the reliable DateTime column
df["Date"] = df["DateTime"].dt.strftime("%d %b %Y")
df["Time"] = df["DateTime"].dt.strftime("%H:%M")


# Calculate the day from DateTime so it is always consistent
df["Day"] = df["DateTime"].dt.day_name()


# Keep the columns needed by the rest of the project
df = df[["DateTime", "Day", "Date", "Time", "load_kwh"]]


# Sort chronologically
df = df.sort_values("DateTime").reset_index(drop=True)


# Save the cleaned data product
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)


print(f"Saved {len(df)} rows to {OUTPUT_FILE}")
print("Columns:", list(df.columns))
print(df.head())
