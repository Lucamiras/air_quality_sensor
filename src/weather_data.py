import datetime
import os
import pandas as pd
import requests

from dotenv import load_dotenv
from pathlib import Path
from tqdm import tqdm

from src.config import load_config


load_dotenv(override=True)
API_KEY = os.getenv("OPEN_WEATHER_MAP_API_KEY")


def create_weather_dataset(
        config_fg: str = "config/config.json"
) -> None:
    """Load OpenWeather data for the location and timestamp
    defined in the config.json file.

    Args:
        config_fg (str, optional): File path of configuration JSON. Defaults to "config/config.json".
        save_to_df (str, optional): File path of data destination. Defaults to "data/weather.parquet".
    """

    cfg = load_config(Path(config_fg))
    Path(cfg.weather_data_fp).parent.mkdir(exist_ok=True)

    if not cfg:
        raise FileNotFoundError("Configuration could not be loaded.")
    
    if not API_KEY:
        raise ValueError("Missing API key!")
    
    records = []
    date_range = pd.date_range(
        start=pd.to_datetime(
            datetime.datetime(
                year=cfg.from_date.year,
                month=cfg.from_date.month,
                day=cfg.from_date.day)),
        end=pd.to_datetime(
            datetime.datetime(
                year=cfg.to_date.year,
                month=cfg.to_date.month,
                day=cfg.to_date.day
            )
        ),
        freq="1h"
    )

    url = "https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={api_key}"

    for dt in tqdm(date_range):
        unix_dt = int(dt.timestamp())
        response = requests.get(url.format(
            lat=cfg.latitude,
            lon=cfg.longitude,
            time=unix_dt,
            api_key=API_KEY
        )).json()
        
        if "data" not in response:
            raise KeyError("Key 'data' not found in response.")
        
        if len(response["data"]) < 1:
            raise Exception("'data' is empty.")
        
        records.append(response["data"][0])

    df = pd.DataFrame(records).reset_index()
    df.to_parquet(Path(cfg.weather_data_fp), index=False)

if __name__ == "__main__":
    create_weather_dataset()



    
