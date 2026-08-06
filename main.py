from pathlib import Path
from battery import Battery
from data_loader import load_data, check_data_quality
from report import (
    create_baseline_report,
    create_overall_summary,
)


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


if __name__ == "__main__":
    print("\nBattery full round-trip efficiency test:")

    battery = Battery()

    # Start at minimum SOC so all delivered energy comes from this test charge.
    battery.soc_kwh = battery.min_soc_kwh

    print("Starting state:", battery.status())

    # Request one hour at the maximum 5 MW charging power.
    grid_energy_charged_kwh = battery.charge(5_000.0)

    print(f"Grid energy used to charge: {grid_energy_charged_kwh:.2f} kWh")
    print("State after charging:", battery.status())

    # Deliver every kWh that can be discharged while preserving minimum SOC.
    requested_discharge_kwh = battery.available_discharge_output_kwh()
    delivered_energy_kwh = battery.discharge(requested_discharge_kwh)

    print(f"Energy delivered from battery: {delivered_energy_kwh:.2f} kWh")
    print("State after full discharge:", battery.status())

    measured_rte = delivered_energy_kwh / grid_energy_charged_kwh

    print(f"Measured round-trip efficiency: {measured_rte:.2%}")
    print(
        "Configured round-trip efficiency: "
        f"{battery.config.round_trip_efficiency:.2%}"
    )

    #main()