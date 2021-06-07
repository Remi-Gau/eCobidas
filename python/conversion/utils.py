import os


def set_dir(this_schema):

    this_path = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(this_path, "..", "..")
    in_dir = os.path.join(
        root_dir,
        "inputs",
        "csv",
    )
    if this_schema in ["neurovault", "pet", "eyetracking", "nimg_reexecution"]:
        sub_dir = this_schema
    elif this_schema in ["all_sequences"]:
        sub_dir = "mri"
    elif this_schema in ["participants", "behavior"]:
        sub_dir = "core"

    if this_schema == "test":
        in_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
        sub_dir = os.path.join("inputs", "csv")

    return in_dir, sub_dir


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
