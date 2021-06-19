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
#   
# schema
#
# core-participants
# core-beh
# core-rep
# core-data
# mri-allseq
# mri-design
# mri-acq
# mri-preproc
# mri-model
# mri-results
# neurovault
# deprecated-mri
# meeg-design
# meeg-acq
# meeg-preproc
# meeg-analysis
# meeg-reporting
# deprecated-meeg
# eyetracking
# pet
# reexecution
# resp-mri_soft
# resp-pres_soft
# resp-multiple_comp
# resp-interp
# resp-cost_functions
# resp-meeg_ref
# resp-meeg_analysis_soft
# resp-meeg_amplifier_brands
# resp-meeg_acq_softwares
# resp-eeg_cap_types
# resp-boolean
# artemis-hardware
# artemis-acquisition
# artemis-preproc
# artemis-design
# artemis-measur
# artemis-channel
# artemis-vis
# test
# resp-ver-spm
# resp-ver-linux
# resp-type-os
# resp-ver-windows
# resp-ver-macos
# resp-eye_preproc_soft
# resp-eye_model
# resp-eye_producer

csv_folder=./inputs/csv/
file=spreadsheet_google_id.tsv

# TODO
# add a way to filter all by section 

if [ $# -lt 1 ]; then
    schema='neurovault'
    else
    schema=$1
fi

google_ID=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $schema | awk '{print $4}'`
subfolder=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $schema | awk '{print $2}'`
output_filename=`cat $csv_folder'spreadsheet_google_id.tsv' | grep $schema | awk '{print $3}'`

ouput_folder="$csv_folder$subfolder/"
mkdir -p $ouput_folder

len=${#google_ID[@]}

# TODO
# add error in case google_ID is empty

for id in $google_ID
do

    echo "Downloading the $subfolder $output_filename spreadsheet to $subfolder/$output_filename"
    echo Google ID: $google_ID
    echo $ouput_folder

    curl -L "https://docs.google.com/spreadsheets/d/"$google_ID"/export?format=tsv" \
        -o $ouput_folder$output_filename.tsv

    echo "Done"

done

