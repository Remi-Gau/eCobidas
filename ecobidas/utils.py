from functools import lru_cache
from pathlib import Path

import pandas as pd
from loguru import logger
from reproschema.models.protocol import Protocol


@lru_cache
def root_dir() -> Path:
    return Path(__file__).parent


@lru_cache
def get_input_dir(source_dir: str | Path = None) -> Path:
    if source_dir is None:
        source_dir = root_dir()
    return Path(source_dir) / "inputs" / "csv"


@lru_cache
def get_output_dir(this_schema: str | Path, out_dir: str | Path) -> Path:
    if Path(this_schema).is_file():
        return Path(out_dir) / Path(this_schema).stem
    schema_info = get_schema_info(this_schema)
    return Path(out_dir) / schema_info["dir"].tolist()[0]


@lru_cache
def get_metatable() -> pd.DataFrame:
    metatable_file = get_input_dir() / "spreadsheet_google_id.tsv"
    return pd.read_csv(metatable_file, sep="\t")


def list_preset_responses() -> list:
    df = get_metatable()
    is_response_option = df["dir"] == "response_options"
    response_options = df[is_response_option]
    return list(response_options["subdir"])


def get_landing_page(schema_info: dict) -> str:
    DEFAULT = ["README_eCOBIDAS-en.md"]

    if schema_info["landing page"].isna().tolist()[0]:
        landing_page = DEFAULT
    else:
        landing_page = list(schema_info["landing page"])

    repo = "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/landing_pages/"
    landing_page = repo + landing_page[0]

    return landing_page


def get_schema_info(this_schema) -> pd.DataFrame:
    df = get_metatable()
    if Path(this_schema).is_file():
        this_schema = Path(this_schema).stem

    logger.debug(f"Loading data for: {this_schema}")

    is_this_schema = df["schema"] == this_schema
    return df[is_this_schema]


def get_input_file(schema_info: dict) -> Path:
    input_dir = root_dir()
    folder = schema_info["dir"].tolist()[0]

    if schema_info["schema"].tolist()[0] == "test":
        input_dir = Path(__file__).parent / "tests"

    input_dir = get_input_dir(input_dir)
    basename = schema_info["basename"].tolist()[0]

    return input_dir / folder / f"{basename}.tsv"


def load_data(this_schema) -> pd.DataFrame:
    input_file = this_schema
    if not Path(this_schema).is_file():
        schema_info = get_schema_info(this_schema)
        input_file = get_input_file(schema_info)

    logger.info(f"\nLoading: {str(input_file)}\n")

    return pd.read_csv(input_file, sep="\t")


def convert_to_str(df_field):
    return df_field.tolist()[0]


def convert_to_int(df_field) -> int:
    return int(df_field.tolist()[0])


def snake_case(input: str) -> str:
    return input.replace("\n", "").replace(" ", "_").replace(",", "")


def print_info(type: str, pref_label: str, file: str) -> None:
    logger.info(
        dashed_line() + "\n" + type.upper() + ": " + pref_label + "\nWill be saved at: " + file
    )


def print_item_info(activity_idx, item_idx, item_info: dict) -> None:
    logger.debug(
        f"Activity: {int(activity_idx)} Item: {int(item_idx)}\t{item_info['name']}\t{item_info['field_type']}\t{item_info['visibility']}"
    )


def print_download(repo: str, branch: str, protocol: Protocol, this_schema) -> None:
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
