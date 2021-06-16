#!/usr/bin/env bash

#  TODO
# Add a loop to download them all
# 
# 
# Simple script to download the content of a specific sheet of a google spreadsheet in
# the inputs folder
# 
# https://stackoverflow.com/questions/27000699/google-spreadsheet-direct-download-link-for-only-one-sheet-as-excel
#
# USAGE:
#
#   sh download_tsv_artemis.sh section subsection
# 
# To know which are the possible comniation of section and subsection
#
#   cat inputs/csv/spreadsheet_google_id.tsv | awk '{print $1, "\t\t" ,$2}
#
# section                  subsection
#
# artemis                  hardware
# artemis                  acquisition
# artemis                  preprocessing
# artemis                  experimental_design_sample
# artemis                  measurements
# artemis                  channel_electrode_choice
# artemis                  visualization

csv_folder=./inputs/csv/
file=spreadsheet_google_id.tsv

# TODO
# add a way to filter all by section 

if [ $# -lt 1 ]; then
    section='artemis'
    else
    section=$1
fi

if [ $# -lt 2 ]; then
    subsection='hardware'
    else
    subsection=$2
fi

ouput_folder="$csv_folder$section/"
mkdir -p $ouput_folder

output_filename=$subsection.tsv

google_ID=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $section | grep $subsection | awk '{print $3}'`
sheet_id=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $section | grep $subsection | awk '{print $4}'`

# TODO
# add error in case google_ID is empty

echo "\nDownloading the $section $subsection spreadsheet to $ouput_folder$output_filename"
echo Google ID: $google_ID

curl -L "https://docs.google.com/spreadsheets/d/"$google_ID"/export?format=tsv&gid="$sheet_id \
    -o $ouput_folder$output_filename

echo "\nDone\n"


return