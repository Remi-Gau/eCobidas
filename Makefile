# ---------------------------------------------------------------------------- #
# 							   CONVERSION TO JSONLD
# ---------------------------------------------------------------------------- #

INPUT_DIR = $(ecobidas/inputs/csv)

ALL_TSV = $(wildcard ecobidas/inputs/csv/*/*.tsv)

NEUROVAULT_TSV =   ecobidas/inputs/csv/neurovault/neurovault.tsv
NEUROVAULT_JSON =  cobidas_schema/schemas/neurovault/protocols/neurovault_schema.jsonld

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

all: neurovault responses pet eye rexec mri

# ---------------------------------------------------------------------------- #
# ARTEMIS
# ---------------------------------------------------------------------------- #
artemis: download_artemis $(ARTEMIS_TSV) validate_artemis

download_artemis: tools/download_subsheet_tsv.sh
	bash tools/download_subsheet_tsv.sh artemis-

convert_artemis: $(ARTEMIS_TSV)
	ecobidas_convert --schema artemis- --out_dir artemis_schema/schemas

# ---------------------------------------------------------------------------- #
# NEUROVAULT
# ---------------------------------------------------------------------------- #
$(NEUROVAULT_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh neurovault

convert_neurovault: $(NEUROVAULT_TSV)
	ecobidas_convert --schema neurovault --out_dir cobidas_schema/schemas

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

$(PET_JSON): $(PET_TSV)
	ecobidas_convert --schema pet

# ---------------------------------------------------------------------------- #
# EYETRACKING
# ---------------------------------------------------------------------------- #
$(EYE_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh eyetracking

$(EYE_JSON): $(EYE_TSV)
	ecobidas_convert --schema eyetracking

# ---------------------------------------------------------------------------- #
# NIMG REEXECUTION
# ---------------------------------------------------------------------------- #
$(REEXEC_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh reexecution

$(REEXEC_JSON): $(REEXEC_TSV)
	ecobidas_convert --schema reexecution

# ---------------------------------------------------------------------------- #
# CORE
# ---------------------------------------------------------------------------- #
download_core: tools/download_tsv.sh
	bash tools/download_tsv.sh core-

convert_core: download_core
	ecobidas_convert --schema core-

# ---------------------------------------------------------------------------- #
# MRI
# ---------------------------------------------------------------------------- #
mri: core clean_mri

download_mri: tools/download_tsv.sh
	bash tools/download_tsv.sh mri-

convert_mri: download_mri
	ecobidas_convert --schema mri-design
	ecobidas_convert --schema mri-allseq
	ecobidas_convert --schema mri-acq
	ecobidas_convert --schema mri-preproc
	ecobidas_convert --schema mri-mass_univariate
	ecobidas_convert --schema mri-multivariate
	ecobidas_convert --schema mri-results

# ---------------------------------------------------------------------------- #
# DOWNLOAD
download_meeg:
	bash tools/download_tsv.sh meeg-

# LINT
remark: package.json
	npx remark *.md docs/*.md --rc-path .remarkrc

package.json:
	npm install `cat npm-requirements.txt`
