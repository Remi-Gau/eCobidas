#!/usr/bin/env bash

# function download_csv {
#     # function check_installed() {
#     #     func=${1}
#     #     hash ${func} 2> /dev/null || {
#     #         printf "Missing software program: ${func}. "
#     #         printf "Check installation instructions\n"
#     #         missing=true
#     #     }
#     # }

#     # csv_name=$1
#     # google_ID=$2
#     echo "download eyetracker spreadsheet to inputs/csv/"$1
#     curl -L "https://docs.google.com/spreadsheets/d/"$2"/export?format=csv" \
#         -o inputs/csv/$1

# }

# download_csv "cobidas_eyetracker.csv" "1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o"
# eyetracker_google_ID=1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o


eyetracker_csv_filename=cobidas_eyetracker.csv
download_csv $eyetracker_google_ID $eyetracker_csv_filename

echo "download eyetracker spreadsheet to inputs/csv/$eyetracker_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$eyetracker_google_ID"/export?format=csv" \
    -o inputs/csv/$eyetracker_csv_filename


mri_google_ID=
mri_csv_filename=cobidas_mri.csv

echo "download eyetracker spreadsheet to inputs/csv/$mri_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$mri_google_ID"/export?format=csv" \
    -o inputs/csv/$mri_csv_filename


meeg_google_ID=
meeg_csv_filename=cobidas_meeg.csv

echo "download eyetracker spreadsheet to inputs/csv/$meeg_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$meeg_google_ID"/export?format=csv" \
    -o inputs/csv/$meeg_csv_filename


neurovault_google_ID=
neurovault_csv_filename=cobidas_neurovault.csv

echo "download eyetracker spreadsheet to inputs/csv/$neurovault_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$neurovault_google_ID"/export?format=csv" \
    -o inputs/csv/$neurovault_csv_filename


pet_google_ID=
pet_csv_filename=cobidas_pet.csv

echo "download eyetracker spreadsheet to inputs/csv/$pet_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$pet_google_ID"/export?format=csv" \
    -o inputs/csv/$pet_csv_filename
