import os
import json


def create_schema(schema_to_create, OUTPUT_DIR):
    """
    This takes the content of the a csv file and turns it into a
    reproschema protocol.
    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encouters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """

    from item import get_item_info

    DEBUG = True

    # -----------------------------------------------------------------------------
    #                                   START
    # -----------------------------------------------------------------------------

    protocol, protocol_path = initialize_protocol(schema_to_create, OUTPUT_DIR)

    df = load_data(schema_to_create)

    activities = df.activity_order.unique()

    if DEBUG:
        activities = [1]

    for activity_idx in activities:

        this_activity = df["activity_order"] == activities[activity_idx - 1]
        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        protocol, activity, activity_path = initialize_activity(
            protocol, items, OUTPUT_DIR
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

    import pandas as pd

    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    csv_dir = os.path.join("inputs", "csv")

    input_file = os.path.join(source_dir, csv_dir, schema_to_create + ".csv")
    return pd.read_csv(input_file)


def initialize_protocol(schema_to_create, OUTPUT_DIR):

    from reproschema_protocol import ReproschemaProtocol

    protocol_name = schema_to_create
    protocol = ReproschemaProtocol()
    protocol.set_defaults(protocol_name)

    # create output directories
    protocol_path = os.path.join(OUTPUT_DIR, "protocols", protocol.dir)
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


def initialize_activity(protocol, items, OUTPUT_DIR):

    from reproschema_activity import ReproschemaActivity

    activity = ReproschemaActivity()

    activity_pref_label = items.activity_pref_label.unique()[0]
    activity.set_pref_label(activity_pref_label)

    activity_name = activity_pref_label.lower().replace(" ", "_")
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

    activity_path = os.path.join(OUTPUT_DIR, "activities", protocol.dir, activity.dir)

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

    from item import define_new_item

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
        + type.upper
        + ": "
        + pref_label
        + "\n"
        + file
        + "\n"
        + "--------------------------------------------------------------"
    )
