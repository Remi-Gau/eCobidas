"""General parser for the cohort_creator package."""

from __future__ import annotations

from argparse import ArgumentParser, HelpFormatter

from ecobidas._version import __version__


def base_parser(formatter_class: type[HelpFormatter] = HelpFormatter) -> ArgumentParser:
    parser = ArgumentParser(
        prog="ecobidas",
        description="Management tool for the ecobidas checklist.",
        formatter_class=formatter_class,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{__version__}",
    )
    return parser


def global_parser(formatter_class: type[HelpFormatter] = HelpFormatter) -> ArgumentParser:
    parser = base_parser(formatter_class=formatter_class)
    subparsers = parser.add_subparsers(
        dest="command",
        help="Choose a subcommand",
        required=True,
    )

    convert_parser = subparsers.add_parser(
        "convert",
        help="""Convert TSVs to JSON-LD.""",
        formatter_class=parser.formatter_class,
    )
    convert_parser.add_argument(
        "-s",
        "--schema",
        help="Name of the schema to create.",
        default="neurovault",
        required=False,
        type=str,
        nargs=1,
    )
    convert_parser.add_argument(
        "-o",
        "--output_dir",
        default="cobidas_schema/schemas",
        help="Where the files will be written on your machine.",
        required=False,
        type=str,
        nargs=1,
    )
    convert_parser.add_argument(
        "-r",
        "--repo",
        default="ohbm/cobidas_schema",
        help="""
        Placeholder of the 'username/repo' that will host the schema representation.
        Example: 'ohbm/cobidas_schema'
        """,
        required=False,
        type=str,
        nargs=1,
    )
    convert_parser.add_argument(
        "-b",
        "--branch",
        default="main",
        help="""
        Placeholder of the 'branch' that will host the schema representation.
        Example: 'remi-dev'
        """,
        required=False,
        type=str,
        nargs=1,
    )
    convert_parser.add_argument(
        "-v",
        "--verbosity",
        help="""
        Verbosity level.
        """,
        required=False,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
    )
    convert_parser.add_argument(
        "--debug",
        action="store_true",
        help="Runs the app in debug mode.",
    )

    update_parser = subparsers.add_parser(
        "update",
        help="Update TSVs by downloading the google sheets.",
        formatter_class=parser.formatter_class,
    )
    update_parser.add_argument(
        "-s",
        "--schema",
        help="Name of the schema to download.",
        default="neurovault",
        required=False,
        type=str,
        nargs=1,
    )
    update_parser.add_argument(
        "-v",
        "--verbosity",
        help="""
        Verbosity level.
        """,
        required=False,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
    )

    serve_parser = subparsers.add_parser(
        "serve",
        help="Launch a local server to serve the JSON-LD files.",
        formatter_class=parser.formatter_class,
    )
    serve_parser.add_argument(
        "folder",
        help="""
        Folder to serve.
        """,
        default="./cobidas_schema/schemas/neurovault/protocols/",
        type=str,
        nargs=1,
    )
    serve_parser.add_argument(
        "-v",
        "--verbosity",
        help="""
        Verbosity level.
        """,
        required=False,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
    )

    return parser
