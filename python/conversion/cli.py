import click
from create_schema import convert_to_schema

# -----------------------------------------------------------------------------
#                                   PARAMETERS
# -----------------------------------------------------------------------------
# modify the following lines to match your needs

# schema_to_create = [
#     "mri_all_sequences",
#     "participants",
#     "behavior",
#     "neurovault",
#     "pet",
#     "mri",
#     "eyetracker",
#     "artemis",
#     "reexec_nimg",
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

branch = "master"


@click.command()
@click.option(
    "--schema_to_create", default="neurovault", help="Name of the schema to create."
)
@click.option(
    "--output_dir",
    default="/home/remi/github/cobidas_chckls",
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
