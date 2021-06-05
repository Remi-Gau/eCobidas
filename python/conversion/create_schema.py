import os
import pandas as pd

from item import get_item_info, define_new_item
from utils import snake_case
from reproschema_protocol import ReproschemaProtocol
from reproschema_activity import ReproschemaActivity


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

            this_item = items[items["item_order"] == index]

            item_info = get_item_info(this_item)

            create_new_item(item_info, activity_path)

            activity.update_activity(item_info)

        activity.sort()
        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.sort()
    protocol.write(protocol_path)

    return protocol


def load_data(schema_to_create):

    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    csv_dir = os.path.join("inputs", "csv")

    if schema_to_create == "test":
        source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")

    input_file = os.path.join(source_dir, csv_dir, schema_to_create + ".csv")
    return pd.read_csv(input_file)


def initialize_protocol(schema_to_create, output_dir):

    protocol_name = snake_case(schema_to_create)
    protocol = ReproschemaProtocol()
    protocol.set_defaults(protocol_name)

    # create output directories
    protocol_path = os.path.join(output_dir, "protocols", protocol.dir)
    protocol.set_directory = protocol_path
    if not os.path.exists(protocol_path):
        os.makedirs(protocol_path)

    protocol.sort()
    protocol.write(protocol_path)

    print_info(
        "activity",
        protocol_name,
        os.path.join(protocol_path, protocol.get_filename()),
    )

    return protocol, protocol_path


def initialize_activity(protocol, items, output_dir):

    activity = ReproschemaActivity()

    activity_pref_label = items.activity_pref_label.unique()[0]
    activity.set_pref_label(activity_pref_label)

    activity_name = snake_case(activity_pref_label)
    activity.set_defaults(activity_name)
    activity.set_filename(activity_name)

    URI = (
        "../../activities/"
        + protocol.get_name()
        + "/"
        + activity.get_name()
        + "/"
        + activity.get_filename()
    )
    activity.set_URI(URI)

    activity_path = os.path.join(output_dir, "activities", protocol.dir, activity.dir)

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

    item.sort()

    item.write(os.path.join(activity_path, "items"))


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
