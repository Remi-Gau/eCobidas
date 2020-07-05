import json
import os
import csv
from protocol import define_new_protocol, update_protocol
from activity import define_new_activity, update_activity
from item import get_item_info, define_new_item

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

# REPRONIM_REPO = "https://raw.githubusercontent.com/ReproNim/reproschema/master/"
REPRONIM_REPO = "https://raw.githubusercontent.com/ReproNim/reproschema/refactor-1.0/"

# ----------------------------------------
# where the checklist csv is. It is in xlsx dir of this repo
# but it can also be downloaded from here:
# https://github.com/NeuroVault/NeuroVault/blob/master/xlsx/

# ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

OUTPUT_DIR = "/home/remi/github/COBIDAS_chckls"
# OUTPUT_DIR = "/home/remi/github/cobidas-PET"

# ----------------------------------------
# Placeholder to insert in all instances of the remote repo that will host the schema representation
# Most likely you just need to replace Remi-Gau in the following line by your github username

REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/COBIDAS_chckls/"
# REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas-PET/"

# ----------------------------------------
# to which branch of reproschema the user interface will be pointed to
# In the end the cobidas-UI repository will be reading the schema from the URL that that
# starts with: REMOTE_REPO + BRANCH

# BRANCH = "master"
# BRANCH = 'neurovault'
# BRANCH = "remi-MRI"
# BRANCH = "PET"
BRANCH = "remi-reproschema_ref1"

# ----------------------------------------
# Protocol info

# Neurovaut
# INPUT_FILE = "/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv"
# protocol = {"name": "neurovault_"}
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
protocol = {"name": "PET_"}
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
# protocol = {"name": "cobidas-MRI_"}
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

protocol = define_new_protocol(REPRONIM_REPO, REMOTE_REPO, BRANCH, protocol, VERSION)

# create output directories
if not os.path.exists(os.path.join(OUTPUT_DIR, "protocols", protocol["dir"])):
    os.makedirs(os.path.join(OUTPUT_DIR, "protocols", protocol["dir"]))

# Initialize this variable as we will need to check if we got to a new section while
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

                activity = define_new_activity(
                    protocol,
                    section,
                    row,
                    CSV_INFO,
                    REMOTE_REPO,
                    BRANCH,
                    REPRONIM_REPO,
                    VERSION,
                )

                # create dir for this section
                if not os.path.exists(
                    os.path.join(OUTPUT_DIR, "activities", activity["name"])
                ):
                    os.makedirs(
                        os.path.join(OUTPUT_DIR, "activities", activity["name"])
                    )
                    os.makedirs(
                        os.path.join(
                            OUTPUT_DIR, "activities", activity["name"], "items"
                        )
                    )

                protocol = update_protocol(activity, protocol)

                print(activity["name"])

            activity = update_activity(activity, item_info)

            # save activity schema and context with every new item
            with open(
                os.path.join(
                    OUTPUT_DIR, "activities", activity["name"], activity["schema_file"]
                ),
                "w",
            ) as ff:
                json.dump(activity["schema"], ff, sort_keys=False, indent=4)

            # -------------------------------------------------------------------
            # Create new item
            # -------------------------------------------------------------------
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
                    row[CSV_INFO["item"]["col"]],
                ),
                "w",
            ) as ff:
                json.dump(item_schema, ff, sort_keys=False, indent=4)

# write protocol jsonld
with open(
    os.path.join(OUTPUT_DIR, "protocols", protocol["dir"], protocol["schema_file"]), "w"
) as ff:
    json.dump(protocol["schema"], ff, sort_keys=False, indent=4)
