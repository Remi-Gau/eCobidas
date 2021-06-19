#!/usr/bin/env bash

schema="core"

IDs=($(awk 'BEGIN{pat="^core"} $0 ~ pat{print $4 }' inputs/csv/spreadsheet_google_id.tsv))

len=${#IDs[@]}
echo $len

for (( i=0; i<$len; i++ ))
do

echo $i
echo "${IDs[$i]}"

done

