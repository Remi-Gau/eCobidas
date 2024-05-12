# TODO
# create another entry point for creating response files
# see how reproschema uses click to create command line calls `reproschema validate`

import os

import click

from ecobidas.create_schema import create_schema
from ecobidas.utils import get_metatable, print_download, root_dir

default_dir = os.path.join(root_dir(), "schemas")

# def set_verbosity(verbosity: int | list[int]) -> None:
#     if isinstance(verbosity, list):
#         verbosity = verbosity[0]
#     if verbosity == 0:
#         log.setLevel("ERROR")
#     elif verbosity == 1:
#         log.setLevel("WARNING")
#     elif verbosity == 2:
#         log.setLevel("INFO")
#     elif verbosity == 3:
#         log.setLevel("DEBUG")


@click.command()
@click.option("--schema", default="neurovault", help="Name of the schema to create.")
@click.option(
    "--out_dir",
    default=default_dir,
    help="Where the files will be written on your machine.",
)
@click.option(
    "--repo",
    default="ohbm/cobidas_schema",
    help="""
    Placeholder of the 'username/repo' that will host the schema representation.
    Example: 'ohbm/cobidas_schema'
    """,
)
@click.option(
    "--branch",
    default="main",
    help="""
    Placeholder of the 'branch' that will host the schema representation.
    Example: 'remi-dev'
    """,
)
def convert(schema, out_dir, repo, branch):
    # TODO
    # If this_schema is a file

    df = get_metatable()

    schema_to_run = df[df["schema"].str.match(f"(^{schema}.*)") == True]
    schema = list(schema_to_run["schema"])

    if isinstance(schema, str):
        schema = [schema]

    for this_schema in schema:
        # add debug parameter
        protocol = create_schema(this_schema, out_dir)

        if "resp" not in this_schema:
            print_download(repo, branch, protocol, this_schema)


if __name__ == "__main__":
    convert()
