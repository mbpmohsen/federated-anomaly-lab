from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw/london-smart-meter")
HOUSEHOLD_INDEX_PATH = Path("data/interim/household_index.csv")

CLIENT_FILE_MAP_PATH = Path("data/interim/client_file_map.csv")

ENERGY_COLUMN_RAW = "KWH/hh (per half hour) "
ENERGY_COLUMN = "KWH/hh (per half hour)"


def summarize_file(
    path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(
        path,
        usecols=[
            "LCLid",
            "stdorToU",
            "DateTime",
            ENERGY_COLUMN_RAW,
        ],
    )

    df.columns = df.columns.str.strip()

    file_map = df[["LCLid"]].drop_duplicates().assign(source_file=path.name)

    df["DateTime"] = pd.to_datetime(
        df["DateTime"],
        errors="coerce",
    )

    df["energy"] = pd.to_numeric(
        df[ENERGY_COLUMN],
        errors="coerce",
    )

    summary = df.groupby(
        ["LCLid", "stdorToU"],
        as_index=False,
    ).agg(
        rows=("LCLid", "size"),
        start=("DateTime", "min"),
        end=("DateTime", "max"),
        invalid_timestamps=("DateTime", lambda x: x.isna().sum()),
        invalid_energy=("energy", lambda x: x.isna().sum()),
        zero_energy=("energy", lambda x: (x == 0).sum()),
        negative_energy=("energy", lambda x: (x < 0).sum()),
    )

    return summary, file_map


def build_index() -> tuple[pd.DataFrame, pd.DataFrame]:
    files = sorted(RAW_DATA_DIR.glob("LCL-June2015v2_*.csv"))

    if not files:
        raise FileNotFoundError(f"No London Smart Meter CSV files found in {RAW_DATA_DIR}")

    summaries = []
    file_maps = []

    for index, path in enumerate(files, start=1):
        print(f"[{index}/{len(files)}] {path.name}")

        summary, file_map = summarize_file(path)

        summaries.append(summary)
        file_maps.append(file_map)

    combined = pd.concat(summaries, ignore_index=True)

    client_file_map = (
        pd.concat(
            file_maps,
            ignore_index=True,
        )
        .drop_duplicates()
        .sort_values(["LCLid", "source_file"])
        .reset_index(drop=True)
    )
    household_index = (
        combined.groupby(["LCLid", "stdorToU"], as_index=False)
        .agg(
            rows=("rows", "sum"),
            start=("start", "min"),
            end=("end", "max"),
            invalid_timestamps=("invalid_timestamps", "sum"),
            invalid_energy=("invalid_energy", "sum"),
            zero_energy=("zero_energy", "sum"),
            negative_energy=("negative_energy", "sum"),
        )
        .sort_values("LCLid")
        .reset_index(drop=True)
    )

    return household_index, client_file_map


def main() -> None:
    household_index, client_file_map = build_index()

    HOUSEHOLD_INDEX_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    household_index.to_csv(
        HOUSEHOLD_INDEX_PATH,
        index=False,
    )

    client_file_map.to_csv(
        CLIENT_FILE_MAP_PATH,
        index=False,
    )

    print("\nDataset index complete")
    print(f"Households: {len(household_index)}")
    print(f"Output: {HOUSEHOLD_INDEX_PATH}")
    print(f"Output: {CLIENT_FILE_MAP_PATH}")

    print("\nTariff distribution:")
    print(household_index["stdorToU"].value_counts())

    print("\nRow-count statistics:")
    print(household_index["rows"].describe())

    print("\nInvalid energy statistics:")
    print(household_index["invalid_energy"].describe())


if __name__ == "__main__":
    main()
