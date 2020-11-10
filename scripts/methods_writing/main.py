import json
import argparse
import os

from template_manager import *


def parse_arguments():
    """Main method to parse the input arguments.

    :return: The object with all the parsed arguments or their default value.
    """

    # Add the parsing of arguments
    parser = argparse.ArgumentParser(
        description='Template-based BIDS report language generation')

    # Add the argument for the parent or root template name
    parser.add_argument('-t', action="store", dest='parent_template_name', default='base_report')

    args = parser.parse_args()

    return args


OUTFILE: str = 'renderedReportResult.txt'

if __name__ == '__main__':

    # Fetch the input arguments
    input_args = parse_arguments()

    # Load the name for the root pattern
    parent_template_name: str = input_args.parent_template_name

    # TODO Parametrize this in arguments, maybe use a processor class
    # Get the input BIDS data
    input_data = json.load(open('data/sample_meg.json'))

    # Initialize the class responsible for rendering templates
    TemplateManager.initialize()

    # Render the root patter, hierarchically rendering all the sub-patterns
    rendered_template: str = TemplateManager.render_template(parent_template_name, input_data=input_data)

    # Print the result in stdout
    print(rendered_template)

    # Output the same result in a text file in the OUTFILE path
    with open(OUTFILE, 'w') as out:
        out.write("{} ".format(rendered_template))


