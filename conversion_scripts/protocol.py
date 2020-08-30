def define_new_protocol(REPRONIM_REPO, REMOTE_REPO, BRANCH, protocol, VERSION):
    # define the jsonld for the schema protocol

    protocol["schema_file"] = protocol["name"] + "schema"
    protocol["context_file"] = protocol["name"] + "context"
    protocol["dir"] = protocol["name"][0:-1]

    protocol["schema"] = {
        "@context": REPRONIM_REPO + "contexts/generic",
        "@type": "reproschema:Protocol",
        "@id": protocol["schema_file"],
        "prefLabel": protocol["schema_file"],
        "description": protocol["schema_file"],
        "schemaVersion": VERSION,
        "version": "0.0.1",
        "landingPage": {"@id": "../README-en.md", "@language": "en"},
        # "image": "mit_voice_pilot_applet_image.svg?sanitize=true",
        "ui": {
            "allow": ["reproschema:AutoAdvance", "reproschema:AllowExport"],
            "shuffle": False,
            "order": [],
            "addProperties": [],
        },
    }

    return protocol


def update_protocol(activity, protocol):

    activity["URI"] = (
        "../../activities/" + activity["name"] + "/" + activity["schema_file"]
    )

    # update the content of the protool schema and context wrt this new activity
    append_to_protocol = {
        "variableName": activity["name"],
        "isAbout": activity["URI"],
        # for the name displayed by the UI for this activity we simply reuse the
        # activity name
        "prefLabel": {"en": activity["pref_label"]},
    }

    protocol["schema"]["ui"]["order"].append(activity["URI"])
    protocol["schema"]["ui"]["addProperties"].append(append_to_protocol)

    return protocol
