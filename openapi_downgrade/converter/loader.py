import json
import yaml
import requests
from pathlib import Path
from datetime import datetime, date

def convert_datetime_objects(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: convert_datetime_objects(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_datetime_objects(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_datetime_objects(item) for item in obj)
    return obj

def load_spec(path_or_url: str) -> dict:
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        response = requests.get(path_or_url)
        response.raise_for_status()
        return _parse_spec(response.text)
    else:
        path = Path(path_or_url)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        with open(path, "r") as f:
            return _parse_spec(f.read())

def _parse_spec(text: str) -> dict:
    try:
        spec = json.loads(text)
    except json.JSONDecodeError:
        spec = yaml.safe_load(text)

    # Convert any datetime objects to ISO strings
    return convert_datetime_objects(spec)
