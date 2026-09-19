from pathlib import Path

import pandas as pd

ENERGY_COLUMN = "KWH/hh (per half hour)"


def inspect_file(path: Path) -> None:
    print("=" * 80)
    print(f"FILE: {path.name}")
    print("=" * 80)

    df = pd.read_csv(path)

    # Normalize column names without modifying the raw file.
    df.columns = df.columns.str.strip()

    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values:")
    print(df.isna().sum())

    print(f"\nUnique households: {df['LCLid'].nunique()}")

    print("\nTariff groups:")
    print(df["stdorToU"].value_counts(dropna=False))

    # Energy validation
    energy = pd.to_numeric(df[ENERGY_COLUMN], errors="coerce")

    print("\nEnergy statistics:")
    print(energy.describe())

    invalid_energy = energy.isna()

    print(f"\nInvalid/missing energy values: {invalid_energy.sum()}")

    if invalid_energy.any():
        print("\nRaw invalid energy values:")
        print(df.loc[invalid_energy, ENERGY_COLUMN].value_counts(dropna=False).head(20))

    print(f"\nZero energy values: {(energy == 0).sum()}")
    print(f"Negative energy values: {(energy < 0).sum()}")

    # Timestamp validation
    timestamps = pd.to_datetime(df["DateTime"], errors="coerce")

    print("\nTimestamp range:")
    print(f"Start: {timestamps.min()}")
    print(f"End:   {timestamps.max()}")
    print(f"Invalid timestamps: {timestamps.isna().sum()}")

    # Inspect the household with the most rows in this chunk.
    client_counts = df["LCLid"].value_counts()
    client_id = client_counts.index[0]

    client = df[df["LCLid"] == client_id].copy()

    client["DateTime"] = pd.to_datetime(
        client["DateTime"],
        errors="coerce",
    )

    client = client.sort_values("DateTime")

    print("\nLargest household in this file:")
    print(f"Client: {client_id}")
    print(f"Rows: {len(client)}")
    print(f"Start: {client['DateTime'].min()}")
    print(f"End:   {client['DateTime'].max()}")
    print(
        "Duplicate timestamps:",
        client["DateTime"].duplicated().sum(),
    )

    diffs = client["DateTime"].diff()

    print("\nTimestamp interval counts:")
    print(diffs.value_counts().head(10))


def main() -> None:
    files = [
        Path("data/raw/london-smart-meter/LCL-June2015v2_0.csv"),
        Path("data/raw/london-smart-meter/LCL-June2015v2_84.csv"),
        Path("data/raw/london-smart-meter/LCL-June2015v2_167.csv"),
    ]

    for path in files:
        inspect_file(path)


if __name__ == "__main__":
    main()
