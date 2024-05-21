# functions to be used by the routes
import json
from functools import lru_cache
from pathlib import Path
from typing import Any


def protocol_url(protocol_name: Path) -> Path:
    return (
        Path(__file__).parents[1]
        / "cobidas_schema"
        / "schemas"
        / protocol_name
        / "protocols"
        / f"{protocol_name}_schema.jsonld"
    )


@lru_cache
def get_protocol(protocol_name: str) -> dict[str, Any]:
    file = protocol_url(protocol_name)
    with open(file) as f:
        content = json.load(f)
    return content


def get_item(file: Path) -> dict[str, Any]:
    with open(file) as f:
        content = json.load(f)
    return content
