import os

import pandas as pd
from rich import print


def get_root_dir():
    this_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(this_path, ".."))


def get_input_dir(dir=get_root_dir()):
    return os.path.abspath(os.path.join(dir, "inputs", "csv"))


def get_output_dir(this_schema, out_dir):
    schema_info = get_schema_info(this_schema)

    return os.path.abspath(os.path.join(out_dir, schema_info["dir"].tolist()[0]))


def get_metatable():
    metatable_file = os.path.join(get_input_dir(), "spreadsheet_google_id.tsv")

    return pd.read_csv(metatable_file, sep="\t")


def list_preset_responses():
    df = get_metatable()
    is_response_option = df["dir"] == "response_options"
    response_options = df[is_response_option]
    return list(response_options["subdir"])


def get_landing_page(schema_info: dict):
    DEFAULT = ["README_eCOBIDAS-en.md"]

    if schema_info["landing page"].isna().tolist()[0]:
        landing_page = DEFAULT
    else:
        landing_page = list(schema_info["landing page"])

    repo = "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/landing_pages/"
    landing_page = repo + landing_page[0]

    return landing_page


def get_schema_info(this_schema):
    df = get_metatable()

    is_this_schema = df["schema"] == this_schema
    return df[is_this_schema]


def get_input_file(schema_info: dict):
    input_dir = get_root_dir()
    dir = schema_info["dir"].tolist()[0]

    if schema_info["schema"].tolist()[0] == "test":
        input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")

    input_dir = get_input_dir(input_dir)
    basename = schema_info["basename"].tolist()[0]

    return os.path.join(input_dir, dir, basename + ".tsv")


def load_data(this_schema):
    if not os.path.isfile(this_schema):
        schema_info = get_schema_info(this_schema)
        input_file = get_input_file(schema_info)

    else:
        input_file = this_schema

    print("[bold green]" + "Loading:" + input_file + "[/bold green]" + "\n")

    return pd.read_csv(input_file, sep="\t")


def convert_to_str(df_field):
    return df_field.tolist()[0]


def convert_to_int(df_field):
    return int(df_field.tolist()[0])


def snake_case(input: str):
    return input.replace("\n", "").replace(" ", "_").replace(",", "")


def print_info(type: str, pref_label: str, file: str):
    print(
        dashed_line()
        + "\n"
        + "[bold red]"
        + type.upper()
        + ": "
        + pref_label
        + "[/bold red]"
        + "\n"
        + file
        + "\n"
        + dashed_line()
    )


def print_item_info(activity_idx, item_idx, item_info: dict):
    print(f"Activity: {int(activity_idx)} Item: {int(item_idx)}")
    print(f"   {item_info['name']}   {item_info['field_type']}   {item_info['visibility']}")


def print_download(repo: str, branch: str, protocol):
    repo = f"https://raw.githubusercontent.com/{repo}"

    s = "/"

    print(
        "\n"
        + dashed_line()
        + "\nYou can view this protocol here:\n"
        + "https://www.repronim.org/reproschema-ui/#/?url="
        + s.join(
            [
                repo,
                branch,
                "schemas",
                protocol.dir,
                "protocols",
                protocol.get_filename(),
            ]
        )
        + dashed_line()
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema"
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema"
        + dashed_line()
        + "\n\n"
    )


def dashed_line():
    return "\n--------------------------------------------------------------"
