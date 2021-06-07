# TODO
# create another entry point for creating response files
# see how reproschema uses click to create command line calls `reproschema validate`

import click, os
from create_schema import convert_to_schema

# "neurovault"
# "pet",
# "eyetracking",
# "nimg_reexecution",
# "behavior",
# "participants",
# "all_sequences",
# "nimg_reexecution",


@click.command()
@click.option("--schema", default="neurovault", help="Name of the schema to create.")
@click.option(
    "--out_dir",
    default="/home/remi/github/cobidas_chckls/schemas",
    help="Where the files will be written on your machine.",
)
@click.option(
    "--repo",
    default="Remi-Gau/eCobidas",
    help="""
    Placeholder of the 'username/repo' that will host the schema representation. 
    Example: 'Remi-Gau/eCobidas'
    """,
)
@click.option(
    "--branch",
    default="remi-dev",
    help="""
    Placeholder of the 'branch' that will host the schema representation. 
    Example: 'remi-dev'
    """,
)
def convert(
    schema,
    out_dir,
    repo,
    branch,
):

    print(schema)

    if isinstance(schema, str):
        schema = [schema]

    for i, this_schema in enumerate(schema):

        print(this_schema)

        if this_schema in ["neurovault", "pet", "eyetracking", "nimg_reexecution"]:
            sub_dir = this_schema
        elif this_schema in ["behavior", "participants"]:
            sub_dir = "core"
        elif this_schema in ["all_sequences"]:
            sub_dir = "mri"
        elif this_schema in ["nimg_reexecution"]:
            sub_dir = "rexecution"
        else:
            print("unknown schema:" + this_schema)
            return

        print(this_schema)

        out_dir = os.path.join(out_dir, sub_dir)

        convert_to_schema(this_schema, out_dir, repo, branch)


if __name__ == "__main__":
    convert()
