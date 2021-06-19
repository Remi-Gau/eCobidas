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

if [ $# -lt 1 ]; then
    schema='neurovault'
    else
    schema=$1
fi

csv_folder="./inputs/csv/"
file="spreadsheet_google_id.tsv"
input_file=$csv_folder$file

# output with awk intos arrays and will loop over google ids to download
# use the first column of the metatable for awk and only take lines that start with this pattern
google_IDs=($(     awk -v schema=$schema 'BEGIN{pattern="^"schema } $0 ~ pattern{print $4}' $input_file))
subfolder=($(      awk -v schema=$schema 'BEGIN{pattern="^"schema } $0 ~ pattern{print $2}' $input_file))
output_filename=($(awk -v schema=$schema 'BEGIN{pattern="^"schema } $0 ~ pattern{print $3}' $input_file))

len=${#google_IDs[@]}

for (( i=0; i<$len; i++ ))
do

    printf "\n"

    echo "Downloading the ${subfolder[$i]} ${output_filename[$i]} spreadsheet to ${subfolder[$i]}/${output_filename[$i]}"
    echo Google ID: "${google_IDs[$i]}"

    ouput_folder="$csv_folder${subfolder[$i]}/"
    mkdir -p $ouput_folder    

    curl -L "https://docs.google.com/spreadsheets/d/${google_IDs[$i]}/export?format=tsv" \
    -o $ouput_folder${output_filename[$i]}.tsv

    printf "DONE\n"

done

