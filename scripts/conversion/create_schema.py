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

    import pandas as pd
    from reproschema_protocol import ReproschemaProtocol
    from reproschema_activity import ReproschemaActivity
    from item import get_item_info

    # -----------------------------------------------------------------------------
    #                                   START
    # -----------------------------------------------------------------------------

    input_file = return_protocol_details(schema_to_create)

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

    print(
        "\n\n"
        + "--------------------------------------------------------------"
        + "\nPROTOCOL: "
        + protocol_name
        + "\n"
        + os.path.join(protocol_path, protocol.get_filename())
        + "\n"
        + "--------------------------------------------------------------"
    )

    # to check if we got to a new section while looping through items
    this_section = ""
    activity = []

    df = pd.read_csv(input_file)

    activities = df.activity_order.unique()

    activities = [1]

    for activity_idx in activities:

        this_activity = df["activity_order"] == activities[activity_idx - 1]

        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        activity_pref_label = items.activity_pref_label.unique()[0]
        activity_name = activity_pref_label.lower().replace(" ", "_")

        activity = ReproschemaActivity()
        activity.set_defaults(activity_name)
        activity.set_filename(activity_name)
        activity.set_pref_label(activity_pref_label)

        # print(activity.get_filename())

        URI = (
            "../../activities/"
            + protocol.get_name()
            + "/"
            + activity.get_name()
            + "/"
            + activity.get_filename()
        )
        activity.set_URI(URI)

        activity_path = os.path.join(
            OUTPUT_DIR, "activities", protocol.dir, activity.dir
        )

        print(
            "\n\n"
            + "--------------------------------------------------------------"
            + "\nACTIVITY: "
            + activity_pref_label
            + "\n"
            + os.path.join(activity_path, activity.get_filename())
            + "\n"
            + "--------------------------------------------------------------"
        )

        items_order = items.item_order.unique()

        for index in items_order:

            this_item = items[items["item_order"] == index]

            item_info = get_item_info(this_item)

            # print(item_info)

            create_new_item(item_info, activity_name, activity_path)

            # item_info["URI"] = "items/" + item_info["name"]

            # append_to_activity = {
            # "variableName": item_info["name"],
            # "isAbout": item_info["URI"],
            # "isVis": item_info["visibility"],
            # "valueRequired": False,
            # }

            # self.schema["ui"]["order"].append(item_info["URI"])
            # self.schema["ui"]["addProperties"].append(append_to_activity)

        # with open(input_file, "r") as csvfile:

        #     for row in PROTOCOL_METADATA:

        #         item_info = get_item_info(row, csv_info)

        #         if item_info["name"] != []:

        #             protocol, activity, this_section = create_update_activity(
        #                 row,
        #                 csv_info,
        #                 protocol,
        #                 activity,
        #                 item_info,
        #                 this_section,
        #                 OUTPUT_DIR,
        #             )

        #             create_new_item(
        #                 item_info,
        #                 activity.get_name(),
        #                 OUTPUT_DIR,
        #             )

        if not os.path.exists(activity_path):
            os.makedirs(activity_path)
            os.makedirs(os.path.join(activity_path, "items"))

        activity.sort()
        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.sort()
    protocol.write(protocol_path)

    return protocol


def return_protocol_details(schema_to_create):

    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
    csv_dir = os.path.join("inputs", "csv")

    input_file = os.path.join(source_dir, csv_dir, schema_to_create + ".csv")

    return input_file


def create_update_activity(
    row, csv_info, protocol, activity, item_info, this_section, OUTPUT_DIR
):

    activity.update_activity(item_info)

    activity.sort()

    activity.write(os.path.join(OUTPUT_DIR, "activities", activity.get_name()))

    return protocol, activity, this_section


def create_new_item(item_info, activity_name, activity_path):

    from item import define_new_item

    print("   " + item_info["name"])
    print("       " + item_info["question"])
    print("       " + item_info["field_type"])

    item = define_new_item(item_info)

    item.sort()

    item.write(os.path.join(activity_path, "items"))
