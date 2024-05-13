#!/usr/bin/env python3
"""Simple script to download the content of the different google spreadsheet in the inputs folder."""
import sys
from pathlib import Path

import requests
from rich import print

from ecobidas.utils import root_dir


# Function to download spreadsheet
def download_spreadsheet(schema, csv_folder: Path, input_file):
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

        print()
        print(f"Downloading the {subfolder} {output_filename} spreadsheet to {output_file}")
        print(f"Google ID: {google_id}")

        response = requests.get(
            f"https://docs.google.com/spreadsheets/d/{google_id}/export?format=tsv"
        )
        if response.status_code == 200:
            with open(output_file, "wb") as tsv_file:
                tsv_file.write(response.content)
            print("DONE")
        else:
            print("Error downloading the spreadsheet.")


# Main function
def main():
    # Default schema
    schema = "neurovault" if len(sys.argv) < 2 else sys.argv[1]
    csv_folder = root_dir() / "inputs" / "csv"
    input_file = csv_folder / "spreadsheet_google_id.tsv"

    download_spreadsheet(schema, csv_folder, input_file)


if __name__ == "__main__":
    main()
