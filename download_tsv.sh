#!/usr/bin/env bash

#  TODO
# Add a loop to download them all

# Simple script to download the content of the different google spreadsheet in
# the inputs folder
#
# USAGE:
#
#   sh download_tsv.sh section subsection
# 
# To know which are the possible comniation of section and subsection
#
#   cat inputs/csv/spreadsheet_google_id.tsv | awk '{print $1, "\t\t" ,$2}
#
# section          subsection
#
# core             participants
# core             behavior
# core             reproducibility
# core             data_sharing
# mri              all_sequences
# mri              design
# mri              acquisition
# mri              preprocessing
# mri              modelling_inference
# mri              results
# neurovault       neurovault
# deprecated       mri
# meeg             design
# meeg             acquisition
# meeg             processing
# meeg             statistical_analysis
# meeg             reporting
# deprecated       meeg
# eyetracking      eyetracking
# pet              pet
# reexecution       reexecution
# response_options	mri_softwares
# response_options	mri_softwares
# response_options	stimulus_presentation_softwares
# response_options	multiple_comparison
# response_options	interpolation
# response_options	cost_function
# response_options	meeg_reference_electrode
# response_options	meeg_analysis_softwares
# response_options	meeg_amplifier_brands
# response_options	meeg_acquisition_softwares
# response_options	eeg_cap_types
# response_options	boolean


csv_folder=./inputs/csv/
file=spreadsheet_google_id.tsv

# TODO
# add a way to filter all by section 

if [ $# -lt 1 ]; then
    section='neurovault'
    else
    section=$1
fi

if [ $# -lt 2 ]; then
    subsection='neurovault'
    else
    subsection=$2
fi

ouput_folder="$csv_folder$section/"
mkdir -p $ouput_folder

output_filename=$subsection.tsv

google_ID=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $section | grep $subsection | awk '{print $4}'`

# TODO
# add error in case google_ID is empty

echo "\nDownloading the $section $subsection spreadsheet to $ouput_folder$output_filename"
echo Google ID: $google_ID

curl -L "https://docs.google.com/spreadsheets/d/"$google_ID"/export?format=tsv" \
    -o $ouput_folder$output_filename

echo "\nDone\n"


return