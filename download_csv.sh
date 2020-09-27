#!/usr/bin/env bash

# Simple script to download the content of the different google spreadsheet in
# the csv folder
#
# USAGE
# sh download_csv.sh modality
# 
# modality can be any of the following 
# - eyetracker 
# - mri
# - meeg 
# - neurovault 
# - pet
#
#
# TODO: loop through the inputed modality
# i.e allow for sh download_csv.sh mri eyetracker

csv_folder=inputs/csv/

if [ $# -lt 1 ]; then
    modalities='eyetracker mri meeg neurovault pet'
    else
    modalities=$1
fi

for modality in $modalities;
do
    output_filename=cobidas_$modality.csv

    google_ID=`cat $csv_folder'spreadsheet_google_id.txt' | grep $modality'_google' |  awk '{print $2}'`

    echo "\nDownloading the $modality spreadsheet to $csv_folder$output_filename"
    echo Google ID: $google_ID

    curl -L "https://docs.google.com/spreadsheets/d/"$google_ID"/export?format=csv" \
        -o $csv_folder$output_filename

    echo "\nDone\n"

done


return