import pandas as pd
from config import SUPPLY_DELIVERY_RATE_PER_KWH

EXPECTED_HOURS_2024 = {
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


def create_baseline_report(data):
    """Create a monthly baseline report from the prepared hourly dataset."""

    required_columns = {
        "month",
        "load_kwh",
        "average_load_kw",
        "is_peak_period",
    }

    missing_columns = required_columns - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

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

    monthly["expected_hours"] = monthly["month"].map(
        EXPECTED_HOURS_2024
    )

    monthly["missing_hours"] = (
        monthly["expected_hours"] - monthly["actual_hours"]
    )

    monthly["coverage_percent"] = (
        monthly["actual_hours"]
        / monthly["expected_hours"]
        * 100
    ).round(2)

    monthly["estimated_energy_cost"] = (
        monthly["measured_energy_kwh"]
        * SUPPLY_DELIVERY_RATE_PER_KWH
    ).round(2)

    monthly["data_quality"] = monthly["coverage_percent"].apply(
        classify_data_quality
    )

    return monthly


def create_overall_summary(data, monthly_report):
    """Create overall measured-data totals and coverage information."""

    total_measured_energy_kwh = data["load_kwh"].sum()
    total_expected_hours = monthly_report["expected_hours"].sum()
    total_actual_hours = monthly_report["actual_hours"].sum()
    total_missing_hours = monthly_report["missing_hours"].sum()

    overall_coverage_percent = (
        total_actual_hours / total_expected_hours * 100
    )

    summary = pd.DataFrame(
        {
            "metric": [
                "Measured energy",
                "Estimated energy cost",
                "Actual hours available",
                "Expected hours",
                "Missing hours",
                "Overall data coverage",
                "Highest observed hourly load",
            ],
            "value": [
                round(total_measured_energy_kwh, 2),
                round(
                    total_measured_energy_kwh
                    * SUPPLY_DELIVERY_RATE_PER_KWH,
                    2,
                ),
                int(total_actual_hours),
                int(total_expected_hours),
                int(total_missing_hours),
                round(overall_coverage_percent, 2),
                round(data["average_load_kw"].max(), 2),
            ],
            "unit": [
                "kWh",
                "USD",
                "hours",
                "hours",
                "hours",
                "%",
                "kW",
            ],
        }
    )

    return summary


def classify_data_quality(coverage_percent):
    """Classify monthly results based on available hourly coverage."""

    if coverage_percent >= 90:
        return "Good"
    if coverage_percent >= 75:
        return "Moderate"
    if coverage_percent >= 50:
        return "Limited"
    return "Very limited"
