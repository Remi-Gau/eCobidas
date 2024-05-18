#!/usr/bin/env python3
"""Download the content of the different google spreadsheet in the inputs folder."""
import json
import sys
from pathlib import Path

import pandas as pd
import requests
from loguru import logger

from ecobidas.utils import root_dir


# Function to download spreadsheet
def download_spreadsheet(schema: str) -> None:
    csv_folder = root_dir() / "inputs"
    input_file = csv_folder / "spreadsheet_google_id.tsv"
    # Read spreadsheet_google_id.tsv
    with open(input_file) as f:
        lines = f.readlines()

    # Initialize lists to store data
    google_IDs = []
    subfolders = []
    output_filenames = []

    # Parse the file
    for line in lines:
        fields = line.split("\t")
        if fields[0].startswith(schema):
            google_IDs.append(fields[3].strip())
            subfolders.append(fields[1].strip())
            output_filenames.append(fields[2].strip())

    # Iterate through entries and download spreadsheets
    for google_id, subfolder, output_filename in zip(google_IDs, subfolders, output_filenames):

        output_folder = csv_folder / subfolder
        output_folder.mkdir(exist_ok=True, parents=True)
        output_file = output_folder / f"{output_filename}.tsv"

        logger.info(
            f"\nDownloading GoogleSheet https://docs.google.com/spreadsheets/d/{google_id} "
            f"for {subfolder}/{output_filename} spreadsheet "
            f"\nto {output_file}"
        )

        response = requests.get(
            f"https://docs.google.com/spreadsheets/d/{google_id}/export?format=tsv"
        )
        if response.status_code == 200:
            with open(output_file, "wb") as tsv_file:
                tsv_file.write(response.content)
        else:
            logger.error("Error downloading the spreadsheet.")

        if "resp" not in schema:
            validate_downloaded_file(output_file)
        logger.info("\nDONE")


def validate_downloaded_file(file: str | Path) -> None:
    """Check that file has the right header."""
    df = pd.read_csv(file, sep="\t")
    df.columns

    data_dictionary_file = root_dir() / "inputs" / "data-dictionary.json"
    with open(data_dictionary_file) as f:
        data_dictionary = json.load(f)

    columns = {x for x in df.columns if "Unnamed:" not in x}

    if missing_keys := set(data_dictionary.keys()) - columns:
        logger.warning(f"\nThe following expected columns are missing: {sorted(missing_keys)}")
    if extra_columns := columns - set(data_dictionary.keys()):
        logger.warning(
            f"\nThe following columns are missing from the data dictionary: {sorted(extra_columns)}"
        )


# Main function
def main() -> None:
    # Default schema
    schema = "neurovault" if len(sys.argv) < 2 else sys.argv[1]
    download_spreadsheet(schema)


if __name__ == "__main__":
    main()
