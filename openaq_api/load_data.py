import os
import time
import pandas as pd

from datetime import datetime
from dateutil.relativedelta import relativedelta
from pathlib import Path
from dotenv import load_dotenv
from openaq import OpenAQ
from pandas import json_normalize

load_dotenv(override=True)


API_KEY = os.getenv("OPENAQ_API_KEY")
SAVE_TO_PATH = Path("data/data.parquet")
LATITUDE = float(os.getenv("LATITUDE"))
LONGITUDE = float(os.getenv("LONGITUDE"))
RADIUS = 500
LIMIT = 20
YEARS = list(range(2025, 2027, 1))
MONTHS = list(range(1, 13, 1))
SENSOR_NAME = "pm25"

id = None
df_list = []

client = OpenAQ(api_key=API_KEY)

locations = client.locations.list(
    coordinates=(LATITUDE, LONGITUDE),
    radius=RADIUS,
    limit=LIMIT,
)

for result in locations.results:
    for sensor in result.sensors:
        if sensor.name.startswith(SENSOR_NAME):
            id = sensor.id
            break

for year in YEARS:
    for month in MONTHS:
        date_from = datetime(year, month, 1)
        date_to = date_from + relativedelta(months=1)
        print(date_from)
        if (year, month) == (2026, 3):
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
df.to_parquet(SAVE_TO_PATH, index=False)

client.close()
