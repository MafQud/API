import json
from pathlib import Path
from typing import Any, Dict


def read_json(*, path: Path) -> Dict[str, Any]:
    """
    Loads a json file in a python dictionary
    """
    with open(path, "r") as json_file:
        data = json.load(json_file)
    return data
