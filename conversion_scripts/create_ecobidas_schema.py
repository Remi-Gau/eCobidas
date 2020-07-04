import json
import os
import csv
from utils import (
    define_activity_context,
    define_new_activity,
    get_item_info,
    define_new_item,
    define_response_choice,
    list_responses_options,
)

# import pandas as pd
import warnings

"""
# This script takes the content of the a csv file and turns it into a reproschema
# protocol.
# This scripts loops through the items of the csv and creates a new reproschema
# activity with every new checklist "section" it encouters: this new activity
# will be added to the protocol.
# Every new item encountered is added to the current activity.
"""

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

REPRONIM_REPO = "https://raw.githubusercontent.com/ReproNim/reproschema/master/"

# ----------------------------------------
# where the checklist csv is. It is in xlsx dir of this repo
# but it can also be downloaded from here:
# https://github.com/NeuroVault/NeuroVault/blob/master/xlsx/

# ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

# OUTPUT_DIR = "/home/remi/github/COBIDAS_chckls"
OUTPUT_DIR = "/home/remi/github/cobidas-PET"

# ----------------------------------------
# Placeholder to insert in all instances of the remote repo that will host the schema representation
# Most likely you just need to replace Remi-Gau in the following line by your github username

# REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/COBIDAS_chckls/"
REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas-PET/"

# ----------------------------------------
# to which branch of reproschema the user interface will be pointed to
# In the end the cobidas-UI repository will be reading the schema from the URL that that
# starts with: REMOTE_REPO + BRANCH

BRANCH = "master"
# BRANCH = 'neurovault'
# BRANCH = "remi-MRI"
# BRANCH = "PET"

# ----------------------------------------
# Protocol info

# Neurovaut
# INPUT_FILE = "/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv"
# PROTOCOL = "neurovault_"
# CSV_INFO = {
#     "section": {"col": 1, "name": ""},
#     "item": {"col": 2, "name": "Item"},
#     "question": {"col": 3, "name": ""},
#     "resp_type": {"col": 4, "name": ""},
#     "choice": {"col": 5, "name": ""},
#     "mandatory": {"col": 6, "name": ""},
#     "include": {"col": [], "name": ""},
#     "vis": {"col": 7, "name": ""},
# }

# PET
INPUT_FILE = "/home/remi/github/COBIDAS_chckls/xlsx/PET_guidelines.csv"
PROTOCOL = "PET_"
CSV_INFO = {
    "section": {"col": 5, "name": "Activity"},
    "act_pref_label": {"col": 6, "name": "Activity pref label"},
    "item": {"col": 7, "name": "Item"},
    "question": {"col": 9, "name": ""},
    "resp_type": {"col": 11, "name": ""},
    "choice": {"col": 12, "name": ""},
    "mandatory": {"col": 14, "name": ""},
    "include": {"col": 21, "name": ""},
    "vis": {"col": 15, "name": ""},
}

# COBIDAS MRI
# INPUT_FILE = "/home/remi/github/COBIDAS_chckls/xlsx/COBIDAS_MRI - clean.csv"
# PROTOCOL = "cobidas-MRI_"
# CSV_INFO = {
#     "section": {"col": 18, "name": ""},
#     "item": {"col": 24, "name": "Item"},
#     "question": {"col": 26, "name": ""},
#     "resp_type": {"col": 28, "name": ""},
#     "choice": {"col": 29, "name": ""},
#     "mandatory": {"col": 15, "name": ""},
#     "include": {"col": 13, "name": ""},
#     "vis": {"col": 30, "name": ""},
# }

# --------------------
# VERSION

VERSION = "0.0.1"

# -----------------------------------------------------------------------------
#                                   START
# -----------------------------------------------------------------------------

# protocol names
PROTOCOL_SCHEMA_FILE = PROTOCOL + "schema"
PROTOCOL_CONTEXT_FILE = PROTOCOL + "context"
PROTOCOL_DIR = PROTOCOL[0:-1]

# create output directories
if not os.path.exists(os.path.join(OUTPUT_DIR, "protocols", PROTOCOL_DIR)):
    os.makedirs(os.path.join(OUTPUT_DIR, "protocols", PROTOCOL_DIR))

# define the jsonld for the schema protocol
PROTOCOL_SCHEMA_JSON = {
    "@context": [
        REPRONIM_REPO + "contexts/generic",
        REMOTE_REPO
        + BRANCH
        + "/protocols/"
        + PROTOCOL_DIR
        + "/"
        + PROTOCOL_CONTEXT_FILE,
    ],
    "@type": "reproschema:Protocol",
    "@id": PROTOCOL_SCHEMA_FILE,
    "prefLabel": PROTOCOL_SCHEMA_FILE,
    "schema:description": PROTOCOL_SCHEMA_FILE,
    "schema:schemaVersion": VERSION,
    "schema:version": VERSION,
    "landingPage": REMOTE_REPO + BRANCH + "/protocols/" + PROTOCOL_DIR + "/README.md",
    "ui": {
        "allow": ["autoAdvance", "allowExport"],
        "shuffle": False,
        "order": [],
        "addProperties": [],
    },
}

# define the jsonld for the context associated to this protocol
PROTOCOL_CONTEXT_JSON = {
    "@context": {
        "@version": 1.1,
        "activity_path": REMOTE_REPO + BRANCH + "/activities/",
    }
}

# Initiliaze this variable as we will need to check if we got to a new section while
# looping through items
this_section = ""

# loop through rows of the csv file and create corresponding jsonld for each item
with open(INPUT_FILE, "r") as csvfile:
    PROTOCOL_METADATA = csv.reader(csvfile)
    for row in PROTOCOL_METADATA:

        item_info = get_item_info(row, CSV_INFO)

        if item_info["name"] != []:

            # -------------------------------------------------------------------
            # detect if this is a new section if so it will create a new activity
            # -------------------------------------------------------------------
            if row[CSV_INFO["section"]["col"]] != this_section:

                # update section name
                this_section = row[CSV_INFO["section"]["col"]]
                section = this_section.replace(" ", "_")

                activity_pref_label = row[CSV_INFO["act_pref_label"]["col"]]

                # where the items of this section will be stored
                activity_dir = PROTOCOL + section

                # names of this section schema and its corresponding jsonld files
                activity_schema_name = PROTOCOL + section

                activity_schema_file = activity_schema_name + "_schema"

                activity_context_file = PROTOCOL + section + "_context"

                # create dir for this section
                if not os.path.exists(
                    os.path.join(OUTPUT_DIR, "activities", activity_dir)
                ):
                    os.makedirs(os.path.join(OUTPUT_DIR, "activities", activity_dir))
                    os.makedirs(
                        os.path.join(OUTPUT_DIR, "activities", activity_dir, "items")
                    )

                activity_at_context, activity_context = define_activity_context(
                    REPRONIM_REPO,
                    REMOTE_REPO,
                    BRANCH,
                    activity_dir,
                    activity_context_file,
                )

                activity_schema = define_new_activity(
                    activity_at_context,
                    activity_schema_file,
                    PROTOCOL,
                    section,
                    VERSION,
                )

                # update the content of the protool schema and context wrt this new activity
                append_to_protocol = {
                    "variableName": activity_schema_name,
                    "isAbout": activity_schema_name,
                    # for the name displayed by the UI for this activity we simply reuse the
                    # activity name
                    "prefLabel": {"en": activity_pref_label},
                }

                PROTOCOL_SCHEMA_JSON["ui"]["order"].append(activity_schema_name)
                PROTOCOL_SCHEMA_JSON["ui"]["addProperties"].append(append_to_protocol)

                PROTOCOL_CONTEXT_JSON["@context"][activity_schema_name] = {
                    "@id": "activity_path:" + activity_dir + "/" + activity_schema_file,
                    "@type": "@id",
                }

                print(activity_schema_name)

            # -------------------------------------------------------------------
            # update the content of the activity schema with new item
            # -------------------------------------------------------------------
            append_to_activity = {
                "variableName": item_info["name"],
                "isAbout": "item_path:" + item_info["name"],
                "isVis": item_info["visibility"],
            }

            activity_schema["ui"]["order"].append(item_info["name"])
            activity_schema["ui"]["addProperties"].append(append_to_activity)

            activity_context["@context"][item_info["name"]] = {
                "@id": "item_path:" + item_info["name"],
                "@type": "@id",
            }

            # save activity schema with every new item
            with open(
                os.path.join(
                    OUTPUT_DIR, "activities", activity_dir, activity_schema_file
                ),
                "w",
            ) as ff:
                json.dump(activity_schema, ff, sort_keys=False, indent=4)

            with open(
                os.path.join(
                    OUTPUT_DIR, "activities", activity_dir, activity_context_file
                ),
                "w",
            ) as ff:
                json.dump(activity_context, ff, sort_keys=False, indent=4)

            # -------------------------------------------------------------------
            # Create new item
            # -------------------------------------------------------------------
            print("   " + item_info["name"])

            if item_info["visibility"] == "":
                warnings.warn("No question for this item.", UserWarning)
            else:
                print("       " + item_info["question"])
            print("       " + item_info["resp_type"])

            item_schema_json = define_new_item(
                activity_at_context, item_info["name"], item_info["question"], VERSION
            )

            inputType, responseOptions = define_response_choice(
                item_info["resp_type"], item_info["choices"]
            )

            item_schema_json["ui"]["inputType"] = inputType
            item_schema_json["responseOptions"] = responseOptions

            # write item schema
            with open(
                os.path.join(
                    OUTPUT_DIR,
                    "activities",
                    activity_dir,
                    "items",
                    row[CSV_INFO["item"]["col"]],
                ),
                "w",
            ) as ff:
                json.dump(item_schema_json, ff, sort_keys=False, indent=4)

# write protocol jsonld
with open(
    os.path.join(OUTPUT_DIR, "protocols", PROTOCOL_DIR, PROTOCOL_SCHEMA_FILE), "w"
) as ff:
    json.dump(PROTOCOL_SCHEMA_JSON, ff, sort_keys=False, indent=4)

with open(
    os.path.join(OUTPUT_DIR, "protocols", PROTOCOL_DIR, PROTOCOL_CONTEXT_FILE), "w"
) as ff:
    json.dump(PROTOCOL_CONTEXT_JSON, ff, sort_keys=False, indent=4)
