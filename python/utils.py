import os, warnings
import pandas as pd


def get_root_dir():

    this_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(this_path, ".."))


def get_metatable():

    metatable_file = os.path.abspath(
        os.path.join(get_root_dir(), "inputs", "csv", "spreadsheet_google_id.tsv")
    )

    return pd.read_csv(metatable_file, sep="\t")


def list_preset_responses():

    df = get_metatable()
    is_response_option = df["section"] == "response_options"
    response_options = df[is_response_option]
    return list(response_options["subsection"])


def get_landing_page(this_schema):

    df = get_metatable()

    is_this_schema = df["subsection"] == this_schema
    this_schema_info = df[is_this_schema]

    if list(this_schema_info["landing page"]) == []:
        DEFAULT = ["README_eCOBIDAS-en.md"]
        landing_page = DEFAULT
    else:
        landing_page = list(this_schema_info["landing page"])

    repo = "https://raw.githubusercontent.com/ohbm/eCOBIDAS/master/landing_pages/"
    landing_page = repo + landing_page[0]

    return landing_page


def set_dir(this_schema, out_dir):

    in_dir = os.path.join(
        get_root_dir(),
        "inputs",
        "csv",
    )

    if this_schema == "test":
        in_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")

    if this_schema in [
        "neurovault",
        "pet",
        "eyetracking",
        "reexecution",
        "response_options",
    ]:
        sub_dir = this_schema
    elif this_schema in ["all_sequences"]:
        sub_dir = "mri"
    elif this_schema in ["participants", "behavior"]:
        sub_dir = "core"
    elif this_schema in list_preset_responses():
        sub_dir = "response_options"
    elif this_schema == "test":
        sub_dir = os.path.join("inputs", "csv")
    else:
        warnings.warn("Unknown target schema: " + this_schema)
        sub_dir = this_schema

    out_dir = os.path.join(out_dir, sub_dir)

    in_dir = os.path.join(in_dir, sub_dir)

    return in_dir, out_dir


def load_data(this_schema, out_dir):

    if not os.path.isfile(this_schema):

        in_dir, out_dir = set_dir(this_schema, out_dir)

        input_file = os.path.join(in_dir, this_schema + ".tsv")

    return pd.read_csv(input_file, sep="\t")


def convert_to_str(df_field):

    return df_field.tolist()[0]


def convert_to_int(df_field):

    return int(df_field.tolist()[0])


def snake_case(input):

    return input.replace("\n", "").replace(" ", "_").replace(",", "")


def print_info(type, pref_label, file):

    print(
        dashed_line()
        + "\n"
        + type.upper()
        + ": "
        + pref_label
        + "\n"
        + file
        + "\n"
        + dashed_line()
    )


def print_item_info(activity_idx, item_idx, item_info):

    print("Activity: " + str(activity_idx) + " Item: " + str(item_idx))
    print("  " + item_info["name"] + "   " + item_info["field_type"])


def print_download(repo, branch, protocol):

    repo = "https://raw.githubusercontent.com/" + repo

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
                "protocols",
                protocol.dir,
                protocol.get_filename(),
            ]
        )
        + dashed_line()
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema"
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema"
        + dashed_line()
        + "\n\n",
    )


def dashed_line():
    return "\n--------------------------------------------------------------"
