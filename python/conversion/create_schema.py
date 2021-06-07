import os, sys
import pandas as pd

from item import get_item_info, define_new_item
from utils import snake_case

local_reproschema = "/home/remi/github/reproschema-py/reproschema/models/"
sys.path.insert(0, local_reproschema)

from reproschema.models.activity import Activity
from reproschema.models.protocol import Protocol

this_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(this_path, "..", "..")
input_dir = os.path.join(
    root_dir,
    "inputs",
    "csv",
)


def convert_to_schema(schema_to_create, output_dir, repo, branch="master"):

    repo = "https://raw.githubusercontent.com/" + repo

    for schema in schema_to_create:

        protocol = create_schema(schema, output_dir)

        s = "/"

        print(
            "\n\n"
            + "---------------------------------------------------------------"
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
            + "\n"
            + "--------------------------------------------------------------"
            + "\n"
            + "https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema"
            + "\n"
            + "https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema"
            + "\n"
            + "--------------------------------------------------------------"
            + "\n\n",
        )


def create_schema(schema_to_create, output_dir, debug=False):
    """
    This takes the content of the a csv file and turns it into a
    reproschema protocol.
    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encouters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """

    protocol, protocol_path = initialize_protocol(schema_to_create, output_dir)

    df = load_data(schema_to_create)

    activities = df.activity_order.unique()

    if debug:
        activities = [1]

    for activity_idx in activities:

        this_activity = df["activity_order"] == activities[activity_idx - 1]
        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        protocol, activity, activity_path = initialize_activity(
            protocol, items, output_dir
        )

        items_order = items.item_order.unique()

        for index in items_order:

            print(activity_idx)
            print(index)

            this_item = items[items["item_order"] == index]

            item_info = get_item_info(this_item)

            item = create_new_item(item_info, activity_path)

            activity.append_item(item)

        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.write(protocol_path)

    return protocol


def load_data(schema_to_create):

    if ~os.path.isfile(schema_to_create):

        this_path = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(this_path, "..", "..")
        input_dir = os.path.join(
            root_dir,
            "inputs",
            "csv",
        )
        if schema_to_create in ["neurovault", "pet", "eyetracking", "nimg_reexecution"]:
            sub_dir = schema_to_create
        elif schema_to_create in ["all_sequences"]:
            sub_dir = "mri"
        elif schema_to_create in ["participants", "behavior"]:
            sub_dir = "core"

        if schema_to_create == "test":
            input_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "tests"
            )
            sub_dir = os.path.join("inputs", "csv")

        input_file = os.path.join(input_dir, sub_dir, schema_to_create + ".tsv")

    return pd.read_csv(input_file, sep="\t")


def initialize_protocol(schema_to_create, output_dir):

    protocol_name = snake_case(schema_to_create)
    protocol = Protocol()
    protocol.set_defaults(protocol_name)

    # create output directories
    protocol_path = os.path.join(output_dir, "protocols")
    protocol.set_directory = protocol_path
    if not os.path.exists(protocol_path):
        os.makedirs(protocol_path)

    protocol.write(protocol_path)

    print_info(
        "protocol",
        protocol_name,
        os.path.join(protocol_path, protocol.get_filename()),
    )

    return protocol, protocol_path


def initialize_activity(protocol, items, output_dir):

    activity = Activity()

    activity_pref_label = items.activity_pref_label.unique()[0]
    activity.set_pref_label(activity_pref_label)

    activity_name = snake_case(activity_pref_label)
    activity.set_defaults(activity_name)
    activity.set_filename(activity_name)

    URI = (
        "../activities"
        + "/"
        + activity.get_basename().replace("_schema", "")
        + "/"
        + activity.get_filename()
    )
    activity.set_URI(URI)

    activity_path = os.path.join(output_dir, "activities", activity.dir)

    if not os.path.exists(activity_path):
        os.makedirs(activity_path)

    if not os.path.exists(os.path.join(activity_path, "items")):
        os.makedirs(os.path.join(activity_path, "items"))

    print_info(
        "activity",
        activity_pref_label,
        os.path.join(activity_path, activity.get_filename()),
    )

    return protocol, activity, activity_path


def create_new_item(item_info, activity_path):

    print("   " + item_info["name"])
    print("       " + item_info["question"])
    print("       " + item_info["field_type"])

    item = define_new_item(item_info)

    item.set_URI(os.path.join("items", item.get_filename()))

    item.write(os.path.join(activity_path, "items"))

    return item


def print_info(type, pref_label, file):

    print(
        "\n"
        + "--------------------------------------------------------------"
        + "\n"
        + type.upper()
        + ": "
        + pref_label
        + "\n"
        + file
        + "\n"
        + "--------------------------------------------------------------"
    )
