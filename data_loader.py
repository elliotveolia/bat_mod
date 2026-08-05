from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "DateTime",
    "Date",
    "Time",
    "Day",
    "load_kwh",
}


def load_data(file_path="data/Grid Import.csv"):
    """Load and prepare the cleaned hourly energy data."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = REQUIRED_COLUMNS - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Convert and validate timestamps
    data["DateTime"] = pd.to_datetime(
        data["DateTime"],
        errors="coerce"
    )
    data = data.dropna(subset=["DateTime"]).copy()

    # Load is already hourly energy in kWh
    data["load_kwh"] = pd.to_numeric(
        data["load_kwh"],
        errors="coerce"
    )
    data = data.dropna(subset=["load_kwh"]).copy()

    # Sort the data in chronological order
    data = data.sort_values("DateTime").reset_index(drop=True)

    # Keep the source day column and create a reliable calculated version
    data["source_day"] = data["Day"].astype(str).str.strip()
    data["day_of_week"] = data["DateTime"].dt.day_name()
    data["weekday_number"] = data["DateTime"].dt.weekday

    # Optional consistency check between source Day and timestamp
    data["day_matches_timestamp"] = (
        data["source_day"].str.lower()
        == data["day_of_week"].str.lower()
    )

    # Additional time fields for analysis
    data["month"] = data["DateTime"].dt.to_period("M").astype(str)
    data["year"] = data["DateTime"].dt.year
    data["hour"] = data["DateTime"].dt.hour

    # G-3 weekday peak-period approximation.
    # This assumes each timestamp represents the beginning of its hour.
    # 08:00 through 20:00 are included; 21:00 begins off-peak.
    data["is_peak_period"] = (
        (data["weekday_number"] < 5)
        & (data["hour"] >= 8)
        & (data["hour"] < 21)
    )

    # Since each interval is one hour, hourly kWh equals the numerical
    # average kW during that interval.
    data["average_load_kw"] = data["load_kwh"]

    return data


def check_data_quality(data):
    """Print basic quality checks for the loaded data."""

    print(f"Rows loaded: {len(data)}")
    print(f"Start: {data['DateTime'].min()}")
    print(f"End: {data['DateTime'].max()}")
    print(f"Duplicate timestamps: {data['DateTime'].duplicated().sum()}")
    print(
        "Day-name mismatches:",
        (~data["day_matches_timestamp"]).sum()
    )

    monthly_counts = (
        data.groupby("month")
        .size()
        .rename("actual_hours")
    )

    print("\nRows by month:")
    print(monthly_counts)
