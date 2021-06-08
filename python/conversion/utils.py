import os
import pandas as pd


def get_root_dir():

    this_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(this_path, "..", ".."))


def list_preset_responses():
    return [
        "mri_softwares",
        "stimulus_presentation_softwares",
        "multiple_comparison",
        "interpolation",
        "cost_function",
        "meeg_reference_electrode",
        "meeg_analysis_softwares",
        "meeg_amplifier_brands",
        "meeg_acquisition_softwares",
        "eeg_cap_types",
        "boolean",
    ]


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
        # TODO throw warning
        print("unknown schema:" + this_schema)
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

    return input.lower().replace("\n", "").replace(" ", "_").replace(",", "")


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

    # print("\n")
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
