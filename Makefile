# ---------------------------------------------------------------------------- #
# 							         INSTALL
# ---------------------------------------------------------------------------- #
# install the local package for ecobidas conversion
# install Reproschema-py from the lib folder
install:
	pip install -e .
	pip install -e ./reproschema-py

# ---------------------------------------------------------------------------- #
# 							   CONVERSION TO JSONLD
# ---------------------------------------------------------------------------- #

INPUT_DIR = $(ecobidas/inputs/csv)

ALL_TSV = $(wildcard ecobidas/inputs/csv/*/*.tsv)

NEUROVAULT_TSV =   ecobidas/inputs/csv/neurovault/neurovault.tsv
NEUROVAULT_JSON =  schemas/neurovault/protocols/neurovault_schema.jsonld

PET_TSV =          ecobidas/inputs/csv/pet/pet.tsv
PET_JSON =         schemas/pet/protocols/pet.jsonld

EYE_TSV =          ecobidas/inputs/csv/eyetracking/eyetracking.tsv
EYE_JSON =         schemas/eyetracking/protocols/eyetracking.jsonld

REEXEC_TSV =       ecobidas/inputs/csv/reexecution/reexecution.tsv
REEXEC_JSON =      schemas/reexecution/protocols/reexecution_schema.jsonld

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
neurovault: clean_neurovault validate_neurovault

clean_neurovault:
	rm -rf $(NEUROVAULT_TSV)
	rm -rf schemas/neurovault/

$(NEUROVAULT_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh neurovault

$(NEUROVAULT_JSON): $(NEUROVAULT_TSV)
	ecobidas_convert --schema neurovault --out_dir cobidas_schema/schemas

# ---------------------------------------------------------------------------- #
# RESPONSES
# ---------------------------------------------------------------------------- #
responses: clean_responses validate_responses

clean_responses:
	rm -rf $(RESPONSES_TSV)
	rm -rf schemas/response_options/

download_responses: tools/download_tsv.sh
	bash tools/download_tsv.sh resp-

convert_responses: download_responses
	ecobidas_convert --schema resp-

# ---------------------------------------------------------------------------- #
# PET
# ---------------------------------------------------------------------------- #
pet: clean_pet validate_pet

clean_pet:
	rm -rf $(PET_TSV)
	rm -rf schemas/pet/

$(PET_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh pet

$(PET_JSON): $(PET_TSV)
	ecobidas_convert --schema pet

# ---------------------------------------------------------------------------- #
# EYETRACKING
# ---------------------------------------------------------------------------- #
eye: clean_eye validate_eye

clean_eye:
	rm -rf $(EYE_TSV)
	rm -rf schemas/eyetracking/

$(EYE_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh eyetracking

$(EYE_JSON): $(EYE_TSV)
	ecobidas_convert --schema eyetracking

# ---------------------------------------------------------------------------- #
# NIMG REEXECUTION
# ---------------------------------------------------------------------------- #
rexec: clean_rexec

clean_rexec:
	rm -rf $(REEXEC_TSV)
	rm -rf schemas/reexecution/

$(REEXEC_TSV): tools/download_tsv.sh
	bash tools/download_tsv.sh reexecution

$(REEXEC_JSON): $(REEXEC_TSV)
	ecobidas_convert --schema reexecution

# ---------------------------------------------------------------------------- #
# CORE
# ---------------------------------------------------------------------------- #
core: clean_core

clean_core:
	rm -rf $(CORE_TSV)
	rm -rf schemas/core

download_core: tools/download_tsv.sh
	bash tools/download_tsv.sh core-

convert_core: download_core
	ecobidas_convert --schema core-

# ---------------------------------------------------------------------------- #
# MRI
# ---------------------------------------------------------------------------- #

mri: core clean_mri

clean_mri:
	rm -rf $(MRI_TSV)
	rm -rf schemas/mri

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
