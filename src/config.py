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
            return validated_model
    except Exception as e:
        print("Error occured:")
        print(e)