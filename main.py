from pathlib import Path
from battery import Battery
from data_loader import load_data, check_data_quality
from report import create_baseline_report, create_overall_summary


INPUT_FILE = "data/Grid Import.csv"

def report_gen():
    MONTHLY_OUTPUT_FILE = Path(
        "outputs/baseline_monthly_summary.csv"
    )
    OVERALL_OUTPUT_FILE = Path(
        "outputs/baseline_overall_summary.csv"
    )

    data = load_data(INPUT_FILE)
    check_data_quality(data)

    monthly_report = create_baseline_report(data)
    overall_summary = create_overall_summary(
        data,
        monthly_report,
    )

    MONTHLY_OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    monthly_report.to_csv(
        MONTHLY_OUTPUT_FILE,
        index=False,
    )

    overall_summary.to_csv(
        OVERALL_OUTPUT_FILE,
        index=False,
    )

    print("\nMonthly baseline report:")
    print(monthly_report.to_string(index=False))

    print("\nOverall baseline summary:")
    print(overall_summary.to_string(index=False))

