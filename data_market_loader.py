from gridstatusio import GridStatusClient
from pathlib import Path
import pandas as pd

collect_data = True

api_file =  "/home/elliotjohnson/Desktop/API"
with open(api_file, "r") as file:
    lines = file.readlines()
    lines = lines[0].strip()
    api_key = lines.split(":", 1)[1].strip()

client = GridStatusClient(api_key)


def fetch_isone_real_time_hourly_lmp(
    start_date,
    end_date,
    output_file="data/isone_rt_houlry_lmp.csv",
    timezone="market",
):
    "Download ISO-NE real-time hourly-final LMP data"

    print("Downloading ISO-NE real-time hourly final LMP data...")
    print(f"Start date: {start_date}")
    print(f"End date:   {end_date}")
    print(f"Timezone:   {timezone}")

    lmp_data = client.get_dataset(
        dataset="isone_lmp_real_time_hourly_final",
        start=start_date,
        end=end_date,
        timezone=timezone,
    )

    if not isinstance(lmp_data, pd.DataFrame):
        raise TypeError(
            "GridStatus did not return a pandas DataFrame. "
            f"Received: {type(lmp_data).__name__}"
        )

    if lmp_data.empty:
        print("Warning: the LMP request returned no rows.")
    else:
        print("\nDownload complete.")
        print(f"Rows: {len(lmp_data):,}")
        print("Columns:", lmp_data.columns.tolist())
        print("\nFirst 10 rows:")
        print(lmp_data.head(10).to_string(index=False))

    if output_file is not None:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        lmp_data.to_csv(output_file, index=False)
        print(f"\nSaved data to: {output_file}")

    return lmp_data

if collect_data:
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    fetch_isone_real_time_hourly_lmp(start_date, end_date)