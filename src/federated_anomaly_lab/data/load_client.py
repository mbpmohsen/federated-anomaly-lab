from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path("data/raw/london-smart-meter")
FILE_MAP_PATH = Path("data/interim/client_file_map.csv")

ENERGY_COLUMN = "KWH/hh (per half hour)"


def load_client(client_id: str) -> pd.DataFrame:
    mapping = pd.read_csv(FILE_MAP_PATH)

    source_files = mapping.loc[
        mapping["LCLid"] == client_id,
        "source_file",
    ].tolist()

    if not source_files:
        raise ValueError(f"Unknown client: {client_id}")

    frames = []

    for filename in source_files:
        path = RAW_DATA_DIR / filename

        df = pd.read_csv(path)
        df.columns = df.columns.str.strip()

        client_rows = df[df["LCLid"] == client_id].copy()

        frames.append(client_rows)

    client = pd.concat(
        frames,
        ignore_index=True,
    )

    client["DateTime"] = pd.to_datetime(
        client["DateTime"],
        errors="coerce",
    )

    client["energy"] = pd.to_numeric(
        client[ENERGY_COLUMN],
        errors="coerce",
    )

    client = client.sort_values("DateTime").reset_index(drop=True)

    return client
