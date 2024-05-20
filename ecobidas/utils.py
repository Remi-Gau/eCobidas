from functools import lru_cache
from pathlib import Path

import pandas as pd
from loguru import logger
from reproschema.models.protocol import Protocol
from ruamel.yaml import YAML

yaml = YAML(typ="safe")


@lru_cache
def root_dir() -> Path:
    return Path(__file__).parent


@lru_cache
def get_input_dir(source_dir: str | Path | None = None) -> Path:
    if source_dir is None:
        source_dir = root_dir()
    return Path(source_dir) / "inputs"


@lru_cache
def get_output_dir(this_schema: str | Path, output_dir: str | Path) -> Path:
    if Path(this_schema).is_file():
        return Path(output_dir) / Path(this_schema).stem
    schema_info = get_schema_info(this_schema)
    return Path(output_dir) / schema_info["dir"]


@lru_cache
def get_spreadsheets_info() -> dict[str, dict[str, str]]:
    """Load info about all the spreadsheets."""
    with open(get_input_dir() / "spreadsheet_google_id.yml") as f:
        spreadsheets_info = yaml.load(f)

    for key in spreadsheets_info:
        if "link" not in spreadsheets_info[key] and "google_id" in spreadsheets_info[key]:
            spreadsheets_info[key]["link"] = (
                "https://docs.google.com/spreadsheets/d/"
                f"{spreadsheets_info[key]['google_id']}/edit?usp=sharing"
            )

    expected_keys = ["dir", "link", "citation", "app_link", "google_id", "landing_page", "repo"]
    for key in spreadsheets_info:
        for check in expected_keys:
            if check not in spreadsheets_info[key]:
                spreadsheets_info[key][check] = ""

    return spreadsheets_info


def get_landing_page(schema_info: dict[str, str]) -> str:
    if schema_info["landing_page"]:
        return schema_info["landing_page"]
    else:
        return "../README_eCOBIDAS-en.md"


def get_schema_info(this_schema: str | Path) -> dict[str, str]:
    spreadsheets_info = get_spreadsheets_info()
    if Path(this_schema).is_file():
        this_schema = Path(this_schema).stem

    logger.debug(f"Loading data for: {this_schema}")

    return spreadsheets_info[this_schema]


def get_input_file(schema_info: dict[str, str]) -> Path:
    input_dir = root_dir()
    folder = schema_info["dir"]

    if schema_info == "test":
        input_dir = Path(__file__).parent / "tests"

    input_dir = get_input_dir(input_dir)
    basename = schema_info["basename"]

    return input_dir / folder / f"{basename}.tsv"


def load_data(this_schema: str) -> pd.DataFrame:
    input_file = this_schema
    if not Path(this_schema).is_file():
        schema_info = get_schema_info(this_schema)
        input_file = get_input_file(schema_info)

    logger.info(f"\nLoading: {str(input_file)}\n")

    return pd.read_csv(input_file, sep="\t")


def convert_to_str(df_field: pd.Series) -> str:
    return df_field.tolist()[0]


def convert_to_int(df_field: pd.Series) -> int:
    return int(df_field.tolist()[0])


def snake_case(input: str) -> str:
    return input.replace("\n", "").replace(" ", "_").replace(",", "")


def print_info(type: str, pref_label: str, file: str) -> None:
    logger.info(
        dashed_line() + "\n" + type.upper() + ": " + pref_label + "\nWill be saved at: " + file
    )


def print_item_info(activity_idx: str, item_idx: str, item_info: dict[str, str]) -> None:
    logger.debug(
        f"Activity: {int(activity_idx)} Item: {int(item_idx)}\t{item_info['name']}\t{item_info['field_type']}\t{item_info['visibility']}"
    )


def print_download(repo: str, branch: str, protocol: Protocol, this_schema: str) -> None:
    repo = f"https://raw.githubusercontent.com/{repo}"

    s = "/"

    logger.info(
        "\n"
        + dashed_line()
        + "\nYou can view this protocol here:\n"
        + "https://www.repronim.org/reproschema-ui/#/?url="
        + s.join(
            [
                repo,
                branch,
                "schemas",
                this_schema,
                "protocols",
                protocol.at_id,
            ]
        )
        + "\n\n"
        + "https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema"
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema"
        + "\n\n"
    )


def dashed_line() -> str:
    return "\n" + "-" * 62
