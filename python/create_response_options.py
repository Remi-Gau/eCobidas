# TODO
# set output directory

import os, sys
import click

from utils import load_data, set_dir, get_root_dir

from reproschema.models.item import ResponseOption

local_reproschema = os.path.join(
    get_root_dir(), "..", "reproschema-py", "reproschema", "models"
)
# sys.path.insert(0, local_reproschema)


@click.command()
@click.option(
    "--filename",
    default="mri_softwares",
    help="Name of the response options to create.",
)
@click.option(
    "--out_dir",
    default=os.path.join(get_root_dir(), "schemas"),
    help="Name of the response options to create.",
)
def create_response_options(filename, out_dir):

    df = load_data(filename, out_dir)

    responses = df.name.unique()

    response_options = ResponseOption()
    response_options.set_defaults()
    response_options.set_filename(filename)
    response_options.set_type("integer")
    response_options.unset("multipleChoice")

    for i, name in enumerate(responses):
        response_options.add_choice(name, i)
        response_options.set_max(i)

    in_dir, out_dir = set_dir("response_options", out_dir)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    response_options.write(out_dir)


if __name__ == "__main__":
    create_response_options()
