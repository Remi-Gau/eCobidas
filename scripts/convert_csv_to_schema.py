import os
from create_schema import create_schema

schema_to_create = "eyetracker"  # "neurovault" "pet" "mri" "eyetracker"

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

# OUTPUT_DIR ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

# curl -L "https://docs.google.com/spreadsheets/d/1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o/export?format=csv" \
#     -o inputs/csv/cobidas_eyetracker.csv


OUTPUT_DIR = "/home/remi/github/cobidas_chckls"
# OUTPUT_DIR = "/home/remi/github/cobidas-PET"
# OUTPUT_DIR = "/home/remi/github/cobidas"
# OUTPUT_DIR = "/home/remi/github/cobidas-eyetracker"

# REMOTE_REPO ----------------------------------------
# Placeholder to insert in all instances of the remote repo that will host the
# schema representation
# Most likely you just need to replace Remi-Gau in the following line by your
# github username

REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas_chckls/"
# REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas-PET/"
# REMOTE_REPO = "https://raw.githubusercontent.com/ohbm/cobidas/"
# REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas-eyetracker/"

# -----------------------------------------------------------------------------
#                                   RUN
# -----------------------------------------------------------------------------

protocol = create_schema(schema_to_create, OUTPUT_DIR)

print(
    "https://www.repronim.org/reproschema-ui/#/?url="
    + os.path.join(
        REMOTE_REPO, "master", "protocols", protocol.dir, protocol.get_filename()
    )
)

# https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema
# https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
# -----------------------------------------------------------------------------
