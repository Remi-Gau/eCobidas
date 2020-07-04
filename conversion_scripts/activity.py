def define_new_activity(
    protocol, section, row, CSV_INFO, REMOTE_REPO, BRANCH, REPRONIM_REPO, VERSION
):
    # define the base json content for the activity

    from activity import define_at_context

    activity = {
        "name": protocol["name"] + section,
        "pref_label": row[CSV_INFO["act_pref_label"]["col"]],
    }

    activity["schema_file"] = activity["name"] + "_schema"
    activity["context_file"] = activity["name"] + "_context"

    activity["context"] = {
        "@context": {
            "@version": 1.1,
            "item_path": REMOTE_REPO
            + BRANCH
            + "/activities/"
            + activity["name"]
            + "/items/",
        }
    }

    activity = define_at_context(REPRONIM_REPO, REMOTE_REPO, BRANCH, activity)

    activity = define_activity_schema(activity, protocol, section, VERSION)

    return activity


def define_at_context(REPRONIM_REPO, REMOTE_REPO, BRANCH, activity):

    activity["at_context"] = [
        REPRONIM_REPO + "contexts/generic",
        REMOTE_REPO
        + BRANCH
        + "/activities/"
        + activity["name"]
        + "/"
        + activity["context_file"],
    ]

    return activity


def define_activity_schema(activity, protocol, section, VERSION):

    activity["schema"] = {
        "@context": activity["at_context"],
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
            "allow": ["skipped"],
            "addProperties": [],
        },
    }

    return activity
