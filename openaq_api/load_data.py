import os
import time
from datetime import datetime
from openaq import OpenAQ
from pandas import json_normalize
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=True)


API_KEY = os.getenv("OPENAQ_API_KEY")
SAVE_TO_PATH = Path("data/data.parquet")
LATITUDE = 48.1544376
LONGITUDE = 11.2114821
RADIUS = 5_000
LIMIT = 20
DT_FROM = datetime(2025, 3, 14)
DT_TO = datetime(2026, 3, 14)
PAGES = 43

client = OpenAQ(api_key=API_KEY)
locations = client.locations.list(
    coordinates=(LATITUDE, LONGITUDE),
    radius=RADIUS,
    limit=LIMIT,
)
loc_ids = [res.id for res in locations.results]
locs = [client.locations.get(id) for id in loc_ids]
ids = [
    sensor.id
    for loc in locs
    for result in loc.results
    for sensor in result.sensors
]

all_measurements = []

for id in ids:
    print("id", id, flush=True, end="-")
    for page_num in range(1, PAGES, 1):
        print("|", flush=True, end="")
        measurements = client \
            .measurements \
            .list(
                sensors_id=id,
                data="hours",
                datetime_from=DT_FROM,
                datetime_to=DT_TO,
                page=page_num
            )
        all_measurements += measurements.dict()['results']
    time.sleep(60.)

df = json_normalize(all_measurements)
df.to_parquet(SAVE_TO_PATH, index=False)

client.close()
