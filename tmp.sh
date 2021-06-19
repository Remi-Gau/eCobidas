#!/usr/bin/env bash

schema="core"

csv_folder="./inputs/csv/"
file="spreadsheet_google_id.tsv"
input_file=$csv_folder$file

# output with awk intos arrays and will loop over google ids to download
google_IDs=($(     awk -v schema=$schema 'BEGIN{pat="^"schema } $0 ~ pat{print $4}' $input_file))
subfolder=($(      awk -v schema=$schema 'BEGIN{pat="^"schema } $0 ~ pat{print $2}' $input_file))
output_filename=($(awk -v schema=$schema 'BEGIN{pat="^"schema } $0 ~ pat{print $3}' $input_file))

len=${#google_IDs[@]}

printf "\nSTART\n\n"

for (( i=0; i<$len; i++ ))
do

    echo "Downloading the ${subfolder[$i]} ${output_filename[$i]} spreadsheet to ${subfolder[$i]}/${output_filename[$i]}"
    echo Google ID: "${google_IDs[$i]}"

    ouput_folder="$csv_folder${subfolder[$i]}/"
    mkdir -p $ouput_folder    

    echo "https://docs.google.com/spreadsheets/d/${google_IDs[$i]}/export?format=tsv"

    curl -L "https://docs.google.com/spreadsheets/d/${google_IDs[$i]}/export?format=tsv" \
    -o $ouput_folder${output_filename[$i]}.tsv

    printf "DONE\n\n"

done

