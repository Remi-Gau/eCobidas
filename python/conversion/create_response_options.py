# TODO
# set output directory

filename = "mri_softwares"

import os, sys
import pandas as pd
import click

local_reproschema = "/home/remi/github/reproschema-py/reproschema/models/"
sys.path.insert(0, local_reproschema)

from reproschema.models.item import ResponseOption

this_path = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.join(this_path, "..", "..")
input_dir = os.path.join(root_dir, "inputs", "csv", "response_options")

response_options_path = os.path.join(root_dir, "response_options")
if not os.path.exists(response_options_path):
    os.makedirs(response_options_path)


@click.command()
@click.option(
    "--filename",
    default=filename,
    help="Name of the response options to create.",
)
def create_response_options(filename):

    df = load_data(filename)

    responses = df.name.unique()

    response_options = ResponseOption()
    response_options.set_defaults()
    response_options.set_filename(filename)
    response_options.set_type("integer")
    response_options.unset("multipleChoice")

    for i, name in enumerate(responses):
        response_options.add_choice(name, i)
        response_options.set_max(i)

    response_options.write(response_options_path)


def load_data(filename):

    input_file = os.path.join(input_dir, filename + ".tsv")
    return pd.read_csv(input_file, sep="\t")


if __name__ == "__main__":
    create_response_options()
