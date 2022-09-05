# Makefile to create the activities and protocols

# Dependency graph can be created with:
#
#   make all -Bnd | make2graph | dot -Tpng -o out.png
#
# witrh https://github.com/lindenb/makefile2graph

.PHONY:


# ---------------------------------------------------------------------------- #
# 							         INSTALL
# ---------------------------------------------------------------------------- #
# install the required python and node packages and
# install the local package for ecobidas conversion
# install the pre-commit hook
# clone Rémi's fork of Reproschema-py and install the local package in the lib folder
install:
	pip install -r requirements.txt
	pip install -r python/requirements.txt
	cd python && pip install -e . && cd ..
	mkdir -p lib && git clone https://github.com/Remi-Gau/reproschema-py.git lib/reproschema-py
	cd lib/reproschema-py && git checkout eCobidas_valid && pip install -e .
	pre-commit install
	npm install `cat npm-requirements.txt`


validate_cff: ## Validate the citation file
	cffconvert --validate

# ---------------------------------------------------------------------------- #
# 							   CONVERSION TO JSONLD
# ---------------------------------------------------------------------------- #

INPUT_DIR = $(inputs/csv)

ALL_TSV = $(wildcard inputs/csv/*/*.tsv)

NEUROVAULT_TSV =   inputs/csv/neurovault/neurovault.tsv
NEUROVAULT_JSON =  schemas/neurovault/protocols/neurovault_schema.jsonld

PET_TSV =          inputs/csv/pet/pet.tsv
PET_JSON =         schemas/pet/protocols/pet.jsonld

EYE_TSV =          inputs/csv/eyetracking/eyetracking.tsv
EYE_JSON =         schemas/eyetracking/protocols/eyetracking.jsonld

REEXEC_TSV =       inputs/csv/reexecution/reexecution.tsv
REEXEC_JSON =      schemas/reexecution/protocols/reexecution_schema.jsonld

ARTEMIS_TSV =   $(wildcard inputs/csv/artemis/*.tsv)
CORE_TSV =      $(wildcard inputs/csv/core/*.tsv)
MRI_TSV =       $(wildcard inputs/csv/mri/*.tsv)
RESPONSES_TSV = $(wildcard inputs/csv/response_options/*.tsv)


all: neurovault responses pet eye rexec mri

# ---------------------------------------------------------------------------- #
# ARTEMIS
# ---------------------------------------------------------------------------- #
artemis: download_artemis $(ARTEMIS_TSV) validate_artemis

download_artemis: download_subsheet_tsv.sh
	bash download_subsheet_tsv.sh artemis-

convert_artemis: $(ARTEMIS_TSV)
	ecobidas_convert --schema artemis-

validate_artemis: convert_artemis
	grep -r  "@context" schemas/artemis | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/artemis
clean_artemis:
	rm -rf $(ARTEMIS_TSV)
	rm -rf schemas/artemis/activities


# ---------------------------------------------------------------------------- #
# NEUROVAULT
# ---------------------------------------------------------------------------- #

neurovault: clean_neurovault validate_neurovault

clean_neurovault:
	rm -rf $(NEUROVAULT_TSV)
	rm -rf schemas/neurovault/

$(NEUROVAULT_TSV): download_tsv.sh
	bash download_tsv.sh neurovault

$(NEUROVAULT_JSON): $(NEUROVAULT_TSV)
	ecobidas_convert --schema neurovault
validate_neurovault: $(NEUROVAULT_JSON)
	grep -r  "@context" schemas/neurovault | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/neurovault
verb.clean_neurovault:
	$(call verb, "clean neurovault")


# ---------------------------------------------------------------------------- #
# RESPONSES
# ---------------------------------------------------------------------------- #
responses: clean_responses validate_responses

clean_responses:
	rm -rf $(RESPONSES_TSV)
	rm -rf schemas/response_options/

download_responses: download_tsv.sh
	bash download_tsv.sh resp-

convert_responses: download_responses
	ecobidas_convert --schema resp-

validate_responses: convert_responses
	grep -r  "@context" schemas/response_options | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/response_options


# ---------------------------------------------------------------------------- #
# PET
# ---------------------------------------------------------------------------- #

pet: clean_pet validate_pet

clean_pet:
	rm -rf $(PET_TSV)
	rm -rf schemas/pet/

$(PET_TSV): download_tsv.sh
	bash download_tsv.sh pet

$(PET_JSON): $(PET_TSV)
	ecobidas_convert --schema pet
validate_pet: $(PET_JSON)
	grep -r  "@context" schemas/pet | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/pet


# ---------------------------------------------------------------------------- #
# EYETRACKING
# ---------------------------------------------------------------------------- #

eye: clean_eye validate_eye

clean_eye:
	rm -rf $(EYE_TSV)
	rm -rf schemas/eyetracking/

$(EYE_TSV): download_tsv.sh
	bash download_tsv.sh eyetracking

$(EYE_JSON): $(EYE_TSV)
	ecobidas_convert --schema eyetracking
validate_eye: $(EYE_JSON)
	grep -r  "@context" schemas/eyetracking | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/eyetracking


# ---------------------------------------------------------------------------- #
# NIMG REEXECUTION
# ---------------------------------------------------------------------------- #

rexec: clean_rexec validate_rexec

clean_rexec:
	rm -rf $(REEXEC_TSV)
	rm -rf schemas/reexecution/

$(REEXEC_TSV): download_tsv.sh
	bash download_tsv.sh reexecution

$(REEXEC_JSON): $(REEXEC_TSV)
	ecobidas_convert --schema reexecution
validate_rexec: $(REEXEC_JSON)
	grep -r  "@context" schemas/reexecution | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/reexecution


# ---------------------------------------------------------------------------- #
# CORE
# ---------------------------------------------------------------------------- #

core: clean_core validate_core

clean_core:
	rm -rf $(CORE_TSV)
	rm -rf schemas/core

download_core: download_tsv.sh
	bash download_tsv.sh core-

convert_core: download_core
	ecobidas_convert --schema core-
validate_core: convert_core
	grep -r  "@context" schemas/core | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/core


# ---------------------------------------------------------------------------- #
# MRI
# ---------------------------------------------------------------------------- #

mri: core clean_mri validate_mri

clean_mri:
	rm -rf $(MRI_TSV)
	rm -rf schemas/mri

download_mri: download_tsv.sh
	bash download_tsv.sh mri-

convert_mri: download_mri
	ecobidas_convert --schema mri-design
	ecobidas_convert --schema mri-allseq
	ecobidas_convert --schema mri-acq
	ecobidas_convert --schema mri-preproc
	ecobidas_convert --schema mri-mass_univariate
	ecobidas_convert --schema mri-multivariate
	ecobidas_convert --schema mri-results
validate_mri: convert_mri
	grep -r  "@context" schemas/mri | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/mri

# ---------------------------------------------------------------------------- #


# DOWNLOAD

download_meeg:
	bash download_tsv.sh meeg-


# VALIDATE
validate_all:
	grep -r  "@context" schemas | cut -d: -f1 | xargs -I fname jsonlint -q fname
	python3 tests/jsonParser.py
	reproschema -l DEBUG validate schemas

# CLEAN

clean_all: clean_rexec clean_pet clean_eye clean_artemis clean_neurovault clean_responses


clean_tsv:
	rm -f $(ALL_TSV)

clean_tests:
	rm -rf python/*/tests/outputs

clean_activities:
	rm -rf schemas/*/activities

# HELPER FUNCTIONS

define verb
	@ echo "_____________________________________________________________"
	@ echo ""
	@ echo "        " $(1)
	@ echo "_____________________________________________________________"
	@ echo ""
endef
