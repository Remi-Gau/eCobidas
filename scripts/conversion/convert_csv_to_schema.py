import os
from create_schema import create_schema

# schema_to_create = ["mri_all_sequences" "participants" "behavior" "neurovault", "pet", "mri", "eyetracker" "artemis"]

schema_to_create = ["eyetracker"]

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

# OUTPUT_DIR ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

OUTPUT_DIR = "/home/remi/github/cobidas_chckls"
# OUTPUT_DIR = "/home/remi/github/cobidas-PET"
# OUTPUT_DIR = "/home/remi/github/cobidas"

# REMOTE_REPO ----------------------------------------
# Placeholder of the remote repo that will host the schema representation.
# Most likely you just need to replace Remi-Gau in the following line by your
# github username

REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/eCobidas/"
# REMOTE_REPO = "https://raw.githubusercontent.com/Remi-Gau/cobidas-PET/"
# REMOTE_REPO = "https://raw.githubusercontent.com/ohbm/cobidas/"

# -----------------------------------------------------------------------------
#                                   RUN
# -----------------------------------------------------------------------------

for schema in schema_to_create:

    protocol = create_schema(schema, OUTPUT_DIR)

    print(
        "\n\n"
        + "---------------------------------------------------------------"
        + "\nYou can view this protocol here:\n"
        + "https://www.repronim.org/reproschema-ui/#/?url="
        + os.path.join(
            REMOTE_REPO, "master", "protocols", protocol.dir, protocol.get_filename()
        )
        + "\n"
        + "--------------------------------------------------------------"
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema"
        + "\n"
        + "https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema"
        + "\n"
        + "--------------------------------------------------------------"
        + "\n\n",
    )
