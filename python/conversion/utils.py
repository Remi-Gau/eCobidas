import os

def set_dir(this_schema):

    this_path = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(this_path, "..", "..")
    input_dir = os.path.join(
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
        input_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "tests"
        )
        sub_dir = os.path.join("inputs", "csv")

    return input_dir, sub_dir

def convert_to_str(df_field):

    return df_field.tolist()[0]


def convert_to_int(df_field):

    return int(df_field.tolist()[0])


def snake_case(input):

    return input.lower().replace("\n", "").replace(" ", "_").replace(",", "")
