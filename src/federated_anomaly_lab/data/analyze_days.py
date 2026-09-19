import pandas as pd

from federated_anomaly_lab.data.load_client import load_client

EXPECTED_SLOTS_PER_DAY = 48


def analyze_client_days(client_id: str) -> pd.DataFrame:
    client = load_client(client_id)

    valid_timestamp = client["DateTime"].notna()

    client["date"] = client["DateTime"].dt.date

    client["on_half_hour_grid"] = (
        valid_timestamp
        & client["DateTime"].dt.minute.isin([0, 30])
        & client["DateTime"].dt.second.eq(0)
        & client["DateTime"].dt.microsecond.eq(0)
    )

    daily = (
        client.dropna(subset=["date"])
        .groupby("date")
        .agg(
            rows=("DateTime", "size"),
            unique_timestamps=("DateTime", "nunique"),
            valid_energy=("energy", lambda values: values.notna().sum()),
            valid_grid=("on_half_hour_grid", "all"),
        )
        .reset_index()
    )

    daily["complete"] = (
        daily["rows"].eq(EXPECTED_SLOTS_PER_DAY)
        & daily["unique_timestamps"].eq(EXPECTED_SLOTS_PER_DAY)
        & daily["valid_energy"].eq(EXPECTED_SLOTS_PER_DAY)
        & daily["valid_grid"]
    )

    return daily
