def define_new_activity(
    protocol, section, row, csv_info, REPRONIM_REPO, VERSION
):
    # define the base json content for the activity

    activity = {
        "name": protocol["name"] + section,
        "pref_label": row[csv_info["act_pref_label"]["col"]],
    }

    activity["schema_file"] = activity["name"] + "_schema"

    activity = define_activity_schema(
        activity, protocol, section, REPRONIM_REPO, VERSION
    )

    return activity


def define_activity_schema(activity, protocol, section, REPRONIM_REPO, VERSION):

    activity["schema"] = {
        "@context": REPRONIM_REPO + "contexts/generic",
        "@type": "reproschema:Activity",
        "@id": activity["schema_file"],
        "prefLabel": protocol["name"] + section,
        "description": protocol["name"] + section,
        "schemaVersion": VERSION,
        "version": "0.0.1",
        "preamble": " ",
        "ui": {"order": [], "shuffle": False, "addProperties": []},
    }

    return activity


def update_activity(activity, item_info):
    # update the content of the activity schema with new item

    item_info["URI"] = "items/" + item_info["name"]

    append_to_activity = {
        "variableName": item_info["name"],
        "isAbout": item_info["URI"],
        "isVis": item_info["visibility"],
    }

    activity["schema"]["ui"]["order"].append(item_info["URI"])
    activity["schema"]["ui"]["addProperties"].append(append_to_activity)

    return activity
