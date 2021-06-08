import os, sys
import pandas as pd

from item import get_item_info, define_new_item
from utils import snake_case, set_dir, print_info, print_item_info, get_root_dir

from reproschema.models.activity import Activity
from reproschema.models.protocol import Protocol

local_reproschema = os.path.join(
    get_root_dir(), "..", "reproschema-py", "reproschema", "models"
)
# sys.path.insert(0, local_reproschema)


def create_schema(this_schema, out_dir, debug=False):
    """
    This takes the content of the a csv file and turns it into a
    reproschema protocol.
    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encouters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """

    protocol, protocol_path = initialize_protocol(this_schema, out_dir)

    df = load_data(this_schema, out_dir)

    activities = df.activity_order.unique()

    if debug:
        activities = [1]

    for activity_idx in activities:

        this_activity = df["activity_order"] == activities[activity_idx - 1]
        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        protocol, activity, activity_path = initialize_activity(
            protocol, items, out_dir
        )

        items_order = items.item_order.unique()

        for item_idx in items_order:

            this_item = items[items["item_order"] == item_idx]

            item_info = get_item_info(this_item)

            print_item_info(activity_idx, item_idx, item_info)

            item = create_new_item(item_info, activity_path)

            activity.append_item(item)

        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.write(protocol_path)

    return protocol


def load_data(this_schema, out_dir):

    if not os.path.isfile(this_schema):

        in_dir, out_dir = set_dir(this_schema, out_dir)

        input_file = os.path.join(in_dir, this_schema + ".tsv")

    return pd.read_csv(input_file, sep="\t")


def initialize_protocol(this_schema, out_dir):

    protocol_name = snake_case(this_schema)
    protocol_name = protocol_name.lower()
    protocol = Protocol()
    protocol.set_defaults(protocol_name)

    # create output directories
    protocol_path = os.path.join(out_dir, "protocols")
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


def initialize_activity(protocol, items, out_dir):

    activity = Activity()

    activity_pref_label = items.activity_pref_label.unique()[0]
    activity.set_pref_label(activity_pref_label)

    activity_name = snake_case(activity_pref_label)
    activity_name = activity_name.lower()
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

    activity_path = os.path.join(out_dir, "activities", activity.dir)

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

    item = define_new_item(item_info)

    item.set_URI(os.path.join("items", item.get_filename()))

    item.write(os.path.join(activity_path, "items"))

    return item
