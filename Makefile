# ---------------------------------------------------------------------------- #
# 							   CONVERSION TO JSONLD
# ---------------------------------------------------------------------------- #

INPUT_DIR = $(ecobidas/inputs/csv)

ALL_TSV = $(wildcard ecobidas/inputs/csv/*/*.tsv)

PET_TSV =          ecobidas/inputs/csv/pet/pet.tsv
PET_JSON =         cobidas_schema/schemas/pet/protocols/pet.jsonld

EYE_TSV =          ecobidas/inputs/csv/eyetracking/eyetracking.tsv
EYE_JSON =         cobidas_schema/schemas/eyetracking/protocols/eyetracking.jsonld

REEXEC_TSV =       ecobidas/inputs/csv/reexecution/reexecution.tsv
REEXEC_JSON =      cobidas_schema/schemas/reexecution/protocols/reexecution_schema.jsonld

ARTEMIS_TSV =   $(wildcard ecobidas/inputs/csv/artemis/*.tsv)
CORE_TSV =      $(wildcard ecobidas/inputs/csv/core/*.tsv)
MRI_TSV =       $(wildcard ecobidas/inputs/csv/mri/*.tsv)
RESPONSES_TSV = $(wildcard ecobidas/inputs/csv/response_options/*.tsv)

all: responses pet eye rexec mri

# ---------------------------------------------------------------------------- #
# ARTEMIS
# ---------------------------------------------------------------------------- #
download_artemis: tools/download_subsheet_tsv.sh
	bash tools/download_subsheet_tsv.sh artemis-

# ---------------------------------------------------------------------------- #
# NEUROVAULT
# ---------------------------------------------------------------------------- #
$(NEUROVAULT_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh neurovault

# ---------------------------------------------------------------------------- #
# RESPONSES
# ---------------------------------------------------------------------------- #
download_responses: tools/download_tsv.sh
	bash tools/download_tsv.sh resp-

convert_responses: download_responses
	ecobidas_convert --schema resp-

# ---------------------------------------------------------------------------- #
# PET
# ---------------------------------------------------------------------------- #
$(PET_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh pet

# ---------------------------------------------------------------------------- #
# EYETRACKING
# ---------------------------------------------------------------------------- #
$(EYE_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh eyetracking

# ---------------------------------------------------------------------------- #
# NIMG REEXECUTION
# ---------------------------------------------------------------------------- #
$(REEXEC_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh reexecution

# ---------------------------------------------------------------------------- #
# CORE
# ---------------------------------------------------------------------------- #
download_core: tools/download_tsv.sh
	bash tools/download_tsv.sh core-

# ---------------------------------------------------------------------------- #
# MRI
# ---------------------------------------------------------------------------- #
mri: core clean_mri

download_mri: tools/download_tsv.sh
	bash tools/download_tsv.sh mri-

# ---------------------------------------------------------------------------- #
# DOWNLOAD
download_meeg:
	bash tools/download_tsv.sh meeg-

# LINT
remark: package.json
	npx remark *.md docs/*.md --rc-path .remarkrc

package.json:
	npm install `cat npm-requirements.txt`
