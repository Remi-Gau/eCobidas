#!/usr/bin/env bash

#  TODO
# refactor to fuse with the regular download script
# 
# 
# Simple script to download the content of a specific sheet of a google spreadsheet in
# the inputs folder
# 
# https://stackoverflow.com/questions/27000699/google-spreadsheet-direct-download-link-for-only-one-sheet-as-excel
#
# USAGE:
#
#   sh download_subshhet_tsv.sh schema-abbreviation
# 
# To know which are the possible comniation of section and subsection
#
#   awk '{print $1}' inputs/csv/spreadsheet_google_id.tsv
#
# schema
#
# artemis-hardware
# artemis-acquisition
# artemis-preproc
# artemis-design
# artemis-measur
# artemis-channel
# artemis-vis


if [ $# -lt 1 ]; then
    schema='artemis-'
    else
    schema=$1
fi

csv_folder="./inputs/csv/"
file="spreadsheet_google_id.tsv"
input_file=$csv_folder$file

# output with awk intos arrays and will loop over google ids to download
# use the first column of the metatable for awk and only take lines that start with this pattern
google_IDs=($(     awk -v schema=$schema 'BEGIN{pattern="^"schema } $0 ~ pattern{print $4}' $input_file))
sheet_id=($(     awk -v schema=$schema 'BEGIN{pattern="^"schema } $0 ~ pattern{print $5}' $input_file))
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

    echo "https://docs.google.com/spreadsheets/d/${google_IDs[$i]}/export?format=tsv&gid=${sheet_id[$i]}"

    curl -L "https://docs.google.com/spreadsheets/d/${google_IDs[$i]}/export?format=tsv&gid=${sheet_id[$i]}" \
    -o $ouput_folder${output_filename[$i]}.tsv

    printf "DONE\n"

done

