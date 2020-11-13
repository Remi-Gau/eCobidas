import json
import argparse
import os

from template_manager import *

MODALITY = "anat"

OUTFILE = "dataset_descriptor-" + MODALITY + ".md"

INPUT_PATH = os.path.join("..", "..", "inputs", "bids_template", "sub-01", "ses-01")


def parse_arguments(MODALITY="base"):
    """Main method to parse the input arguments.

    :return: The object with all the parsed arguments or their default value.
    """

    report = MODALITY + "_report"

    # Add the parsing of arguments
    parser = argparse.ArgumentParser(
        description="Template-based BIDS report language generation"
    )

    # Add the argument for the parent or root template name
    parser.add_argument(
        "-t", action="store", dest="parent_template_name", default=report
    )

    return parser.parse_args()


if __name__ == "__main__":

    # Fetch the input arguments
    input_args = parse_arguments(MODALITY)

    # Load the name for the root pattern
    parent_template_name: str = input_args.parent_template_name

    # TODO Parametrize this in arguments, maybe use a processor class

    # Get the input BIDS data

    if MODALITY == "meg":
        input_file = "sub-01_task-FullExample_acq-CTF_run-1_proc-sss_meg.json"
    if MODALITY == "eeg":
        input_file = "sub-01_ses-01_task-FullExample_eeg.json"
    elif MODALITY == "anat":
        input_file = "sub-01_ses-01_acq-FullExample_run-01_T1w.json"
    elif MODALITY == "func":
        input_file = "sub-01_ses-01_task-FullExample_run-01_bold"
    elif MODALITY == "fmap":
        input_file = "sub-01_ses-01_task-FullExample_run-01_bold"
    elif MODALITY == "dwi":
        print("Diffusion weighted imaging not supported")
        # input_file = "sub-01_ses-01_task-FullExample_run-01_bold"
    else:
        input_file = "sub-01_task-FullExample_acq-CTF_run-1_proc-sss_meg.json"

    input_data = json.load(open(os.path.join(INPUT_PATH, MODALITY, input_file)))

    # Initialize the class responsible for rendering templates
    TemplateManager.initialize()

    # Render the root patter, hierarchically rendering all the sub-patterns
    rendered_template: str = TemplateManager.render_template(
        parent_template_name, input_data=input_data
    )

    # Print the result in stdout
    print(rendered_template)

    # Output the same result in a text file in the OUTFILE path
    with open(OUTFILE, "w") as out:
        out.write("{} ".format(rendered_template))
