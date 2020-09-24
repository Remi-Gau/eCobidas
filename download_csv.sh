#!/usr/bin/env bash

# Simple script to download the content of the different google spreadsheet in
# the inputs/csv folder


# ---------------------------------------------------------------------------- #
#                                    eyetracker
#
# https://docs.google.com/spreadsheets/d/1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o/edit?usp=sharing
eyetracker_google_ID=1aQZINzS24oYDgu6PZ8djqZQZ2s2eNs2xP6kyzHokU8o
eyetracker_csv_filename=cobidas_eyetracker.csv

echo "download eyetracker spreadsheet to inputs/csv/$eyetracker_csv_filename"
curl -L "https://docs.google.com/spreadsheets/d/"$eyetracker_google_ID"/export?format=csv" \
    -o inputs/csv/$eyetracker_csv_filename
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                    MRI
#
# https://docs.google.com/spreadsheets/d/1dCXP0MTK3DjY09ZFd7FXgv0Ngx16_YJwVBiXOeQbTho/edit?usp=sharing
# mri_google_ID=1dCXP0MTK3DjY09ZFd7FXgv0Ngx16_YJwVBiXOeQbTho
# mri_csv_filename=cobidas_mri.csv

# echo "download MRI spreadsheet to inputs/csv/$mri_csv_filename"
# curl -L "https://docs.google.com/spreadsheets/d/"$mri_google_ID"/export?format=csv" \
#     -o inputs/csv/$mri_csv_filename
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                    MEEG
#
# https://docs.google.com/spreadsheets/d/1OhkmbtgIWdFxSVjpu6A8PWoAuqev0jY-98GFQlwBCy0/edit?usp=sharing
# meeg_google_ID=1OhkmbtgIWdFxSVjpu6A8PWoAuqev0jY-98GFQlwBCy0
# meeg_csv_filename=cobidas_meeg.csv

# echo "download MEEG spreadsheet to inputs/csv/$meeg_csv_filename"
# curl -L "https://docs.google.com/spreadsheets/d/"$meeg_google_ID"/export?format=csv" \
#     -o inputs/csv/$meeg_csv_filename
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                 neurovault
#
# https://docs.google.com/spreadsheets/d/1arizMF2GnaiXz9txY5tzTU7uoA0_ENE17W5wDeUPpu0/edit?usp=sharing
# neurovault_google_ID=1arizMF2GnaiXz9txY5tzTU7uoA0_ENE17W5wDeUPpu0
# neurovault_csv_filename=cobidas_neurovault.csv

# echo "download neurovault spreadsheet to inputs/csv/$neurovault_csv_filename"
# curl -L "https://docs.google.com/spreadsheets/d/"$neurovault_google_ID"/export?format=csv" \
#     -o inputs/csv/$neurovault_csv_filename
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                                    PET
#
# https://docs.google.com/spreadsheets/d/1HS-1KOP8nE7C3MHiyRmQ6hd823cBZnCRVq0UryXvDc8/edit?usp=sharing
# pet_google_ID=1HS-1KOP8nE7C3MHiyRmQ6hd823cBZnCRVq0UryXvDc8
# pet_csv_filename=cobidas_pet.csv

# echo "download pet spreadsheet to inputs/csv/$pet_csv_filename"
# curl -L "https://docs.google.com/spreadsheets/d/"$pet_google_ID"/export?format=csv" \
#     -o inputs/csv/$pet_csv_filename
# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- #
#                              WORK IN PROGRESS
# ---------------------------------------------------------------------------- #

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