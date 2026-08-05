import pandas as pd

INTERVAL_HOURS = 1.0

data = pd.read_csv("Grid Import.csv")

print("Columns found:", list(data.columns))
print(data.head())

data["timestamp"] = pd.to_datetime(
    data["Date"].astype(str) + " " + data["Time"].astype(str),
    errors="coerce"
)

data["load_kw"] = pd.to_numeric(data["Load_kWhr"], errors="coerce")

data = data.dropna(subset=["timestamp", "load_kw"])
data = data.sort_values("timestamp")

data["month"] = data["timestamp"].dt.to_period("M").astype(str)
data["weekday"] = data["timestamp"].dt.weekday
data["hour"] = data["timestamp"].dt.hour

data["is_peak_period"] = (
    (data["weekday"] < 5) &
    (data["hour"] >= 8) &
    (data["hour"] < 21)
)

data["energy_kwh"] = data["load_kw"] * INTERVAL_HOURS

monthly_energy = (
    data.groupby("month")
    .agg(
        total_energy_kwh=("energy_kwh", "sum"),
        average_load_kw=("load_kw", "mean"),
        interval_count=("load_kw", "count")
    )
    .reset_index()
)

peak_data = data[data["is_peak_period"]]

monthly_peak = (
    peak_data.groupby("month")
    .agg(
        highest_recorded_hourly_load_kw=("load_kw", "max"),
        peak_interval_count=("load_kw", "count")
    )
    .reset_index()
)

baseline = monthly_energy.merge(monthly_peak, on="month", how="left")
baseline["highest_recorded_hourly_load_kw"] = baseline[
    "highest_recorded_hourly_load_kw"
].fillna(0)

baseline.to_csv("baseline_monthly_summary.csv", index=False)

print("\nBaseline monthly summary:")
print(baseline.to_string(index=False))

print("\nAnnual total energy:", round(data["energy_kwh"].sum(), 2), "kWh")
print("Highest recorded load:", round(data["load_kw"].max(), 2), "kW")