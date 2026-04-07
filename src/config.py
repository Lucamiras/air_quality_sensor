import datetime
import json
from pathlib import Path
from pydantic import BaseModel, ConfigDict


class Date(BaseModel):
    year: int
    month: int
    day: int


class Config(BaseModel):
    model_config = ConfigDict(strict=True)
    latitude: float
    longitude: float
    radius: int
    limit: int
    sensor_name: str
    from_date: Date
    to_date: Date
    openaq_data_fp: str
    weather_data_fp: str
    merged_data_fp: str


def load_config(config_fp: Path) -> Config:
    """Load data load configuration from local JSON file.

    Args:
        config_fp (Path): Path to the configuration file in the repository.

    Returns:
        Config: Pydantic model.
    """
    try:
        with open(config_fp, "r") as f:
            json_content = json.loads(f.read())
            validated_model = Config.model_validate(json_content)
            if not _dates_valid(validated_model.from_date, validated_model.to_date):
                raise Exception("'from' and 'to' dates do not allow for valid range.")
            return validated_model
    except Exception as e:
        print("Error occured:")
        print(e)


def _dates_valid(date_1: Date, date_2: Date) -> bool:
    """Check if from_date and to_date allow for a valid date range.

    Args:
        date_1 (datetime.datetime): from_date
        date_2 (datetime.datetime): to_date

    Returns:
        bool: True if dates are valid, else False
    """
    try:
        date_1 = datetime.datetime(date_1.year, date_1.month, date_1.day)

        date_2 = datetime.datetime(date_2.year, date_2.month, date_2.day)

    except ValueError as e:
        print(f"Error parsing dates: {e}")

    dates_valid = True
    
    if date_1 >= date_2:
        dates_valid = False
    
    if (date_1 or date_2) < datetime.datetime(1970, 1, 1):
        dates_valid = False 

    return dates_valid