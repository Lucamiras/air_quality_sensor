import os
import pandas as pd

import datetime
from pathlib import Path

from src.air_quality_data import create_openaq_dataset
from src.config import load_config
from src.weather_data import create_weather_dataset


def create_merged_dataset(
        use_existing_files: bool,
        config_fp: str = "config/config.json"
        ) -> None:
    """Creates a merged dataset ready for model building.

    Args:
        use_existing_files (bool): True if OpenAQ data and Open Weather Map data 
        with matching timestamps already exist.
    """
    if not use_existing_files:
        try:
            create_openaq_dataset()
        except Exception as e:
            print("Failed to create OpenAQ dataset.")
            print(e)
        try:
            create_weather_dataset()
        except Exception as e:
            print("Failed to create Open Weather dataset.")
            print(e)

    cfg = load_config(Path(config_fp))

    if not cfg:
        raise FileNotFoundError("Configuration could not be loaded.")
    
    openaq_data = pd.read_parquet(Path(cfg.openaq_data_fp))
    openweather_data = pd.read_parquet(Path(cfg.weather_data_fp))
    print(openaq_data.shape, openweather_data.shape)

    openaq_data["timestamp"] = pd.to_datetime(
        openaq_data["coverage.datetime_from.utc"],
        utc=True
        )
    
    openweather_data["timestamp"] = openweather_data["dt"] \
        .apply(lambda x: datetime.datetime.fromtimestamp(
            x,
            tz=datetime.timezone.utc)
            )

    date_range = pd.DataFrame(
        {
            "timestamp": pd.date_range(
                start=datetime.datetime(
                    cfg.from_date.year,
                    cfg.from_date.month,
                    cfg.from_date.day),
                end=datetime.datetime(
                    cfg.to_date.year,
                    cfg.to_date.month,
                    cfg.to_date.day),
                freq="1h",
                tz=datetime.timezone.utc
            )
        }
    )
    print(date_range.shape)

    openaq_on_timestamp = pd.merge(
        date_range,
        openaq_data,
        how="left",
        on="timestamp"
    )

    merged_data = pd.merge(
        openaq_on_timestamp,
        openweather_data,
        how="left",
        on="timestamp"
    )

    merged_data = merged_data[[
        'value', 'timestamp', 'temp', 'feels_like', 'pressure',
        'humidity', 'dew_point', 'wind_speed', 'wind_deg',
        'wind_gust'
        ]]
    
    merged_data.to_parquet(cfg.merged_data_fp)


if __name__ == "__main__":
    create_merged_dataset(use_existing_files=True)


    