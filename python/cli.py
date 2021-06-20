# TODO
# create another entry point for creating response files
# see how reproschema uses click to create command line calls `reproschema validate`

import os, click
from create_schema import create_schema
from utils import print_download, get_root_dir, get_metatable

default_dir = os.path.join(get_root_dir(), "schemas")


@click.command()
@click.option("--schema", default="neurovault", help="Name of the schema to create.")
@click.option(
    "--out_dir",
    default=default_dir,
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
def convert(schema, out_dir, repo, branch):

    # TODO
    # If this_schema is a file

    df = get_metatable()

    schema_to_run = df[df["schema"].str.match(r"(^" + schema + ".*)") == True]
    schema = list(schema_to_run["schema"])

    if isinstance(schema, str):
        schema = [schema]

    for this_schema in schema:

        # add debug parameter
        protocol = create_schema(this_schema, out_dir)

        if "resp" not in this_schema:
            print_download(repo, branch, protocol)


if __name__ == "__main__":
    convert()
