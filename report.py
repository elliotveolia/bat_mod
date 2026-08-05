import pandas as pd


def create_baseline_report(data):
    """Create a monthly baseline report from loaded hourly data."""

    monthly = (
        data.groupby("month")
        .agg(
            measured_energy_kwh=("load_kwh", "sum"),
            average_hourly_load_kw=("average_load_kw", "mean"),
            highest_observed_load_kw=("average_load_kw", "max"),
            actual_hours=("load_kwh", "count"),
            peak_period_hours=("is_peak_period", "sum"),
        )
        .reset_index()
    )

    # Expected number of calendar hours in each month of leap year 2024
    expected_hours = {
        "2024-01": 744,
        "2024-02": 696,
        "2024-03": 744,
        "2024-04": 720,
        "2024-05": 744,
        "2024-06": 720,
        "2024-07": 744,
        "2024-08": 744,
        "2024-09": 720,
        "2024-10": 744,
        "2024-11": 720,
        "2024-12": 744,
    }

    monthly["expected_hours"] = monthly["month"].map(expected_hours)
    monthly["missing_hours"] = (
        monthly["expected_hours"] - monthly["actual_hours"]
    )
    monthly["coverage_percent"] = (
        monthly["actual_hours"]
        / monthly["expected_hours"]
        * 100
    ).round(2)

    return monthly
