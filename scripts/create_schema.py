def create_schema(schema_to_create, OUTPUT_DIR, REMOTE_REPO):
    """
    This takes the content of the a csv file and turns it into a
    reproschema protocol.
    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encouters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """

    import json
    import os
    import csv
    from protocol import define_new_protocol
    from item import get_item_info

    REPRONIM_REPO = "https://raw.githubusercontent.com/ReproNim/reproschema/1.0.0-rc1/"
    VERSION = "1.0.0-rc1"

    # -----------------------------------------------------------------------------
    #                                   START
    # -----------------------------------------------------------------------------

    input_file, csv_info = return_protocol_details(schema_to_create)

    protocol = {"name": "cobidas_" + schema_to_create + "_"}
    protocol = define_new_protocol(REPRONIM_REPO, protocol, VERSION)

    # create output directories
    if not os.path.exists(os.path.join(OUTPUT_DIR, "protocols", protocol["dir"])):
        os.makedirs(os.path.join(OUTPUT_DIR, "protocols", protocol["dir"]))

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
                    REPRONIM_REPO,
                    VERSION,
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

    # write protocol jsonld
    with open(
        os.path.join(OUTPUT_DIR, "protocols", protocol["dir"], protocol["schema_file"]),
        "w",
    ) as ff:
        json.dump(protocol["schema"], ff, sort_keys=False, indent=4)

    return protocol


def return_protocol_details(schema_to_create):

    import os
    import json

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
    row,
    csv_info,
    protocol,
    activity,
    item_info,
    this_section,
    OUTPUT_DIR,
    REPRONIM_REPO,
    VERSION,
):

    import os
    import json
    from protocol import update_protocol
    from activity import define_new_activity, update_activity

    # -------------------------------------------------------------------
    # detect if this is a new section if so it will create a new activity
    # -------------------------------------------------------------------
    if row[csv_info["section"]["col"]] != this_section:

        # update section name
        this_section = row[csv_info["section"]["col"]]
        section = this_section.replace(" ", "_")

        activity = define_new_activity(
            protocol, section, row, csv_info, REPRONIM_REPO, VERSION,
        )

        # create dir for this section
        if not os.path.exists(os.path.join(OUTPUT_DIR, "activities", activity["name"])):
            os.makedirs(os.path.join(OUTPUT_DIR, "activities", activity["name"]))
            os.makedirs(
                os.path.join(OUTPUT_DIR, "activities", activity["name"], "items")
            )

        protocol = update_protocol(activity, protocol)

        print(activity["name"])

    activity = update_activity(activity, item_info)

    # save activity schema with every new item
    with open(
        os.path.join(
            OUTPUT_DIR, "activities", activity["name"], activity["schema_file"],
        ),
        "w",
    ) as ff:
        json.dump(activity["schema"], ff, sort_keys=False, indent=4)

    return protocol, activity, this_section


def create_new_item(
    item_info, activity, row, csv_info, OUTPUT_DIR, REPRONIM_REPO, VERSION
):

    import os
    import json
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
