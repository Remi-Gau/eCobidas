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

    import csv
    from reproschema_protocol import ReproschemaProtocol
    from item import get_item_info

    REPRONIM_REPO = "https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc1/"
    VERSION = "1.0.0-rc1"

    # -----------------------------------------------------------------------------
    #                                   START
    # -----------------------------------------------------------------------------

    input_file, csv_info = return_protocol_details(schema_to_create)

    protocol_name = "cobidas_" + schema_to_create
    protocol = ReproschemaProtocol()
    protocol.set_defaults(protocol_name)

    # create output directories
    if not os.path.exists(os.path.join(OUTPUT_DIR, "protocols", protocol.dir)):
        os.makedirs(os.path.join(OUTPUT_DIR, "protocols", protocol.dir))

    # to check if we got to a new section while looping through items
    this_section = ""
    activity = []

    with open(input_file, "r") as csvfile:
        PROTOCOL_METADATA = csv.reader(csvfile)
        for row in PROTOCOL_METADATA:

            item_info = get_item_info(row, csv_info)

            if item_info["name"] != []:

                protocol, activity, this_section = create_update_activity(
                    row,
                    csv_info,
                    protocol,
                    activity,
                    item_info,
                    this_section,
                    OUTPUT_DIR,
                )

                create_new_item(
                    item_info,
                    activity,
                    row,
                    csv_info,
                    OUTPUT_DIR,
                    REPRONIM_REPO,
                    VERSION,
                )

    protocol.write(os.path.join(OUTPUT_DIR, "protocols", protocol.dir))

    return protocol


def return_protocol_details(schema_to_create):

    source_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    csv_dir = os.path.join("inputs", "csv")

    input_file = os.path.join(
        source_dir, csv_dir, "cobidas_" + schema_to_create + ".csv"
    )
    data_dictionnary_file = os.path.join(
        source_dir, csv_dir, "cobidas_" + schema_to_create + ".json"
    )

    with open(data_dictionnary_file) as f:
        csv_info = json.load(f)

    return input_file, csv_info


def create_update_activity(
    row, csv_info, protocol, activity, item_info, this_section, OUTPUT_DIR
):

    from reproschema_activity import ReproschemaActivity

    # -------------------------------------------------------------------
    # detect if this is a new section if so it will create a new activity
    # -------------------------------------------------------------------
    if row[csv_info["section"]["col"]] != this_section:

        # update section name
        this_section = row[csv_info["section"]["col"]]
        section = this_section.replace(" ", "_")

        activity = ReproschemaActivity()

        activity_name = protocol.get_name + section
        activity.set_defaults(activity_name)

        pref_label = row[csv_info["act_pref_label"]["col"]]
        activity.set_pref_label(pref_label)

        URI = "../../activities/" + activity.get_name + "/" + activity.filename
        activity.set_URI(URI)

        # create dir for this section
        if not os.path.exists(
            os.path.join(OUTPUT_DIR, "activities", activity.filename)
        ):
            os.makedirs(os.path.join(OUTPUT_DIR, "activities", activity.filename))
            os.makedirs(
                os.path.join(OUTPUT_DIR, "activities", activity.filename, "items")
            )

        protocol.append_activity(activity)

        print(activity.filename)

    activity.update_activity(activity, item_info)

    # save activity schema with every new item
    activity.write(os.path.join(OUTPUT_DIR, "activities", activity["name"]))

    return protocol, activity, this_section


def create_new_item(
    item_info, activity, row, csv_info, OUTPUT_DIR, REPRONIM_REPO, VERSION
):

    from item import define_new_item

    print("   " + item_info["name"])
    print("       " + item_info["question"])
    print("       " + item_info["resp_type"])

    item_schema = define_new_item(item_info, REPRONIM_REPO, VERSION)

    # write item schema
    with open(
        os.path.join(
            OUTPUT_DIR,
            "activities",
            activity["name"],
            "items",
            row[csv_info["item"]["col"]],
        ),
        "w",
    ) as ff:
        json.dump(item_schema, ff, sort_keys=False, indent=4)
