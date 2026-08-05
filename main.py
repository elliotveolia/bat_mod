from data_loader import check_data_quality, load_data


data = load_data("data/Grid Import.csv")
check_data_quality(data)

print("\nLoaded columns:")
print(data.columns.tolist())

print("\nFirst five rows:")
print(data.head())