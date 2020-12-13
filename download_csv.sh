#!/usr/bin/env bash

# Simple script to download the content of the different google spreadsheet in
# the csv folder
#
# USAGE
# sh download_csv.sh spreadsheet_name
# 
# spreadsheet_name can be any of the following: 
#   participants 
#   behavior 
#   data_sharing 
#   reproducibility 
#   mri_all_sequences
#   mri_acquisition
#   mri_design
#   mri_preprocessing
#   mri_modelling_inference
#   mri_results
#   neurovault
#   meeg_design
#   meeg_acquisition
#   meeg_processing
#   meeg_statistical_analysis
#   meeg_reporting
#   artemis
#   eyetracker
#   pet

csv_folder=inputs/csv/

if [ $# -lt 1 ]; then
    spreadsheet_name='participants behavior data_sharing reproducibility mri_all_sequences mri_acquisition mri_design mri_preprocessing mri_modelling_inference mri_results neurovault meeg_design meeg_acquisition meeg_processing meeg_statistical_analysis meeg_reporting artemis eyetracker pet'
    else
    spreadsheet_name=$1
fi

for modality in $spreadsheet_name;
do
    output_filename=$modality.csv

    google_ID=`cat $csv_folder'spreadsheet_google_id.txt' | grep $modality'_google' |  awk '{print $2}'`

    echo "\nDownloading the $modality spreadsheet to $csv_folder$output_filename"
    echo Google ID: $google_ID

    curl -L "https://docs.google.com/spreadsheets/d/"$google_ID"/export?format=csv" \
        -o $csv_folder$output_filename

    echo "\nDone\n"

done


return