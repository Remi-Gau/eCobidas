# TODO
# create another entry point for creating response files
# see how reproschema uses click to create command line calls `reproschema validate`

import click
from create_schema import convert_to_schema

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

# default_schema = "behavior"
# default_schema = "participants"
# default_output_dir = "/home/remi/github/cobidas_chckls/schemas/core"

# default_schema = "all_sequences"
# default_output_dir = "/home/remi/github/cobidas_chckls/schemas/mri"

# default_schema = "nimg_reexecution"
# default_output_dir = "/home/remi/github/cobidas_chckls/schemas/rexecution"

default_schema = "pet"
default_output_dir = "/home/remi/github/cobidas_chckls/schemas/pet"

# default_schema = "neurovault"
# default_output_dir = "/home/remi/github/cobidas_chckls/schemas/neurovault"

# default_schema = "eyetracking"
# default_output_dir = "/home/remi/github/cobidas_chckls/schemas/eyetracking"

# schema_to_create = [
#     "all_sequences",
#     "participants",
#     "behavior",
#     "mri",
#     "artemis",
# ]

# output_dir ----------------------------------------
# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted

# output_dir = "/home/remi/github/cobidas-PET"
# output_dir = "/home/remi/github/cobidas"
# output_dir = "/home/remi/github/reexecute_nimg_checklist/"

# repo ----------------------------------------
# Placeholder of the remote repo that will host the schema representation.
# Most likely you just need to replace Remi-Gau in the following line by your
# github username

# repo = "https://raw.githubusercontent.com/Remi-Gau/cobidas-PET/"
# repo = "https://raw.githubusercontent.com/ohbm/cobidas/"
# repo = "https://raw.githubusercontent.com/Remi-Gau/reexecute_nimg_checklist/"


@click.command()
@click.option(
    "--schema_to_create", default=default_schema, help="Name of the schema to create."
)
@click.option(
    "--output_dir",
    default=default_output_dir,
    help="Where to output stuff.",
)
@click.option(
    "--repo",
    default="Remi-Gau/eCobidas/",
    help="repo",
)
@click.option("--branch", default="master", help="branch")
def convert(
    schema_to_create,
    output_dir,
    repo,
    branch,
):

    schema_to_create = [schema_to_create]
    convert_to_schema(schema_to_create, output_dir, repo, branch)


if __name__ == "__main__":
    convert()
