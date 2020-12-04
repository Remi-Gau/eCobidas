#!/usr/bin/env bash

# Simple script to validate the schema jsonld file in a folder and print which
#   file is validated.
#
# USAGE
# sh validate_folder.sh folder
# 

if [ $# -lt 1 ]; then
    folder=`echo pwd`
    else
    folder=$1
fi

files=`ls $folder`

for file in $files;
do

echo "\n"
echo $folder$file
reproschema -l DEBUG validate $folder$file

done

return