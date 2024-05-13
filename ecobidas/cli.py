import sys
from typing import Sequence

from loguru import logger
from rich_argparse import RichHelpFormatter

from ecobidas.create_schema import create_schema
from ecobidas.parsers import global_parser
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
        convert(schema, output_dir, repo, branch)
        exit(0)

    if args.command in ["update"]:
        # debug = getattr(args, "debug", True)
        # update(debug=debug)
        exit(0)


def convert(schema, output_dir, repo, branch):

    logger.debug(f"{schema=}, {output_dir=}, {repo=}, {branch=}")

    df = get_metatable()

    schema_to_run = df[df["schema"].str.match(f"(^{schema}.*)") == True]
    schema = list(schema_to_run["schema"])

    if isinstance(schema, str):
        schema = [schema]

    for this_schema in schema:
        # add debug parameter
        protocol = create_schema(this_schema, output_dir)

        if "resp" not in this_schema:
            print_download(repo, branch, protocol, this_schema)


if __name__ == "__main__":
    convert()
