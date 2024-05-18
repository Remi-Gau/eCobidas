import sys
from typing import Sequence

from loguru import logger
from rich_argparse import RichHelpFormatter

from ecobidas.create_schema import create_schema
from ecobidas.download_tsv import download_spreadsheet
from ecobidas.parsers import global_parser
from ecobidas.serve import serve
from ecobidas.utils import get_metatable, print_download


def set_verbosity(verbosity: int | list[int]) -> None:
    logger.remove()
    if isinstance(verbosity, list):
        verbosity = verbosity[0]
    if verbosity == 0:
        level = "ERROR"
    elif verbosity == 1:
        level = "WARNING"
    elif verbosity == 2:
        level = "INFO"
    elif verbosity == 3:
        level = "DEBUG"
    logger.add(sys.stderr, level=level)


def cli(argv: Sequence[str] = sys.argv) -> None:
    parser = global_parser(formatter_class=RichHelpFormatter)

    args, unknowns = parser.parse_known_args(argv[1:])
    if unknowns:
        logger.error(f"The following arguments are unknown: {unknowns}")
        exit(1)

    verbosity = args.verbosity
    set_verbosity(verbosity)

    if args.command in ["convert"]:
        schema = args.schema[0]
        output_dir = args.output_dir
        repo = args.repo
        branch = args.branch
        # debug = getattr(args, "debug", False)
        if isinstance(output_dir, list):
            output_dir = output_dir[0]
        convert(schema, output_dir, repo, branch)
        exit(0)

    if args.command in ["update"]:
        schema = args.schema[0]
        download_spreadsheet(schema=schema)
        exit(0)

    if args.command in ["serve"]:
        folder = args.folder if args.folder is None else args.folder[0]
        serve(folder=folder)
        exit(0)


def convert(schema: str, output_dir: str, repo: str, branch: str) -> None:

    logger.debug(f"{schema=}, {output_dir=}, {repo=}, {branch=}")

    df = get_metatable()

    schema_to_run = df[df["schema"].str.match(f"(^{schema}.*)") == True]
    schema_list = list(schema_to_run["schema"])

    for this_schema in schema_list:
        # add debug parameter
        protocol = create_schema(this_schema, output_dir)

        if "resp" not in this_schema:
            print_download(repo, branch, protocol, this_schema)
