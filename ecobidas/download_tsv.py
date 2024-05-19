#!/usr/bin/env python3
"""Download the content of the different google spreadsheet in the inputs folder."""
import json
from pathlib import Path

import pandas as pd
import requests
from loguru import logger

from ecobidas.utils import get_input_dir, get_spreadsheets_info


# Function to download spreadsheet
def download_spreadsheet(schema: str, output_dir: Path = None) -> None:

    if output_dir is None:
        output_dir = get_input_dir()

    spreadsheets_info = get_spreadsheets_info()

    # Initialize lists to store data
    google_IDs = []
    subfolders = []
    output_filenames = []

    # Parse the file
    for spreadsheet, values in spreadsheets_info.items():
        if spreadsheet.startswith(schema):
            google_IDs.append(values["google_id"])
            subfolders.append(values["dir"])
            output_filenames.append(values["basename"])

    # Iterate through entries and download spreadsheets
    for google_id, subfolder, output_filename in zip(google_IDs, subfolders, output_filenames):

        output_folder = output_dir / subfolder
        output_folder.mkdir(exist_ok=True, parents=True)
        output_file = output_folder / f"{output_filename}.tsv"

        logger.info(
            f"\nDownloading GoogleSheet https://docs.google.com/spreadsheets/d/{google_id} "
            f"\nfor {subfolder}/{output_filename} spreadsheet "
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
        print()


def validate_downloaded_file(file: str | Path) -> None:
    """Check that file has the right header."""
    if file.parent.stem == "response_options":
        return

    print()
    logger.info(f"Validating: {file}")

    df = pd.read_csv(file, sep="\t")

    data_dictionary_file = get_input_dir() / "data-dictionary.json"
    with open(data_dictionary_file) as f:
        data_dictionary = json.load(f)

    columns = {x for x in df.columns if "Unnamed:" not in x}

    required_keys = {
        value["VariableName"]
        for value in data_dictionary.values()
        if value.get("RequirementLevel") == "required"
    }
    recommended_keys = {
        value["VariableName"]
        for value in data_dictionary.values()
        if value.get("RequirementLevel") == "recommended"
    }

    if missing_keys := required_keys - columns:
        logger.error(f"\nThe following expected columns are missing: {sorted(missing_keys)}")

    if missing_keys := recommended_keys - columns:
        logger.warning(f"\nThe following recommended columns are missing: {sorted(missing_keys)}")

    if extra_columns := columns - set(data_dictionary.keys()):
        logger.info(
            f"\nThe following columns are missing from the data dictionary: {sorted(extra_columns)}"
        )


def main() -> None:
    # validates files
    tsv_files = get_input_dir().glob("*/*.tsv")
    for file in tsv_files:
        validate_downloaded_file(file)


if __name__ == "__main__":
    main()
