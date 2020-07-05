def define_new_activity(
    protocol, section, row, CSV_INFO, REMOTE_REPO, BRANCH, REPRONIM_REPO, VERSION
):
    # define the base json content for the activity

    activity = {
        "name": protocol["name"] + section,
        "pref_label": row[CSV_INFO["act_pref_label"]["col"]],
    }

    activity["schema_file"] = activity["name"] + "_schema"

    activity = define_activity_schema(
        activity, protocol, section, REPRONIM_REPO, REMOTE_REPO, BRANCH, VERSION
    )

    return activity


def define_activity_schema(
    activity, protocol, section, REPRONIM_REPO, REMOTE_REPO, BRANCH, VERSION
):

    activity["schema"] = {
        "@context": [
            REPRONIM_REPO + "contexts/generic",
            {
                "item_path": REMOTE_REPO
                + BRANCH
                + "/activities/"
                + activity["name"]
                + "/items/"
            },
        ],
        "@type": "reproschema:Activity",
        "@id": activity["schema_file"],
        "skos:prefLabel": protocol["name"] + section,
        "schema:description": protocol["name"] + section,
        "schema:schemaVersion": VERSION,
        "schema:version": VERSION,
        "preamble": " ",
        "ui": {
            "order": [],
            "shuffle": False,
            "allow": ["reproschema:Skipped"],
            "addProperties": [],
        },
    }

    return activity


def update_activity(activity, item_info):
    # update the content of the activity schema with new item

    item_info["URI"] = "item_path:" + item_info["name"]

    append_to_activity = {
        "variableName": item_info["name"],
        "isAbout": item_info["URI"],
        "isVis": item_info["visibility"],
    }

    activity["schema"]["ui"]["order"].append(item_info["URI"])
    activity["schema"]["ui"]["addProperties"].append(append_to_activity)

    return activity
