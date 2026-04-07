import os
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
from dotenv import load_dotenv
from openaq import OpenAQ
from pandas import json_normalize

from src.config import load_config


load_dotenv(override=True)

API_KEY = os.getenv("OPENAQ_API_KEY")

def create_openaq_dataset(config_fp: str = "config/config.json") -> None:
    """Load OpenAQ data for the location and timestamp
    defined in the config.json file.

    Args:
        config_fp (str, optional): File path of configuration JSON. Defaults to "../config/config.json".
        save_to_df (str, optional): File path of data destination. Defaults to "../data/data.parquet".
    """

    cfg = load_config(Path(config_fp))
    Path(cfg.openaq_data_fp).parent.mkdir(exist_ok=True)

    if not cfg:
        raise FileNotFoundError("Configuration could not be loaded.")
    
    if not API_KEY:
        raise ValueError("Missing API key!")

    years = list(range(cfg.from_date.year, cfg.from_date.year + 1, 1))
    months = list(range(1, 13, 1))
    
    id = None
    df_list = []

    client = OpenAQ(api_key=API_KEY)

    locations = client.locations.list(
        coordinates=(cfg.latitude, cfg.longitude),
        radius=cfg.radius,
        limit=cfg.limit,
    )

    for result in locations.results:
        for sensor in result.sensors:
            if sensor.name.startswith(cfg.sensor_name):
                id = sensor.id
                break

    for year in years:
        for month in months:
            date_from = datetime(year, month, 1)
            date_to = date_from + relativedelta(months=1)
            print(date_from)
            if (year, month) == (cfg.to_date.year, cfg.to_date.month):
                break
            measurements = client.measurements.list(
                sensors_id=id,
                data="hours",
                datetime_from=date_from,
                datetime_to=date_to
            )
            df_temp = json_normalize(measurements.dict()["results"])
            df_list.append(df_temp)

    df = pd.concat(df_list).reset_index()
    df.to_parquet(Path(cfg.openaq_data_fp), index=False)

    client.close()

if __name__ == "__main__":
    create_openaq_dataset()