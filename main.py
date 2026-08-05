from data_loader import load_data, check_data_quality
from report import create_baseline_report


def main():
    data = load_data("data/Grid Import.csv")
    check_data_quality(data)

    baseline = create_baseline_report(data)
    baseline.to_csv(
        "baseline_monthly_summary.csv",
        index=False
    )

    print("\nBaseline report:")
    print(baseline.to_string(index=False))


if __name__ == "__main__":
    main()