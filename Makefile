# Makefile to create the activities and protocols

.PHONY: clean_neurovault

# INSTALL
# TODO
# pip install -r requirements.txt
# git clone https://github.com/Remi-Gau/reproschema-py.git  ../../
# cd ../../reproschema-py
# git checkout remi_schema_creator

# DOWNLOAD and CREATE and VALIDATE

artemis:
	clean_artemis
	bash download_subsheet_tsv.sh artemis-
	ecobidas_convert --schema artemis-hardware
	ecobidas_convert --schema artemis-design
	ecobidas_convert --schema artemis-measur
	ecobidas_convert --schema artemis-channel
	ecobidas_convert --schema artemis-vis
	ecobidas_convert --schema artemis-acquisition
	ecobidas_convert --schema artemis-preproc	
	grep -r  "@context" schemas/artemis | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/artemis


inputs/csv/neurovault/neurovault.tsv:
	bash download_tsv.sh neurovault
neurovault:
	rm -rf inputs/csv/neurovault
	rm -rf schemas/neurovault/
	bash download_tsv.sh neurovault
	ecobidas_convert --schema neurovault
	grep -r  "@context" schemas/neurovault | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/neurovault


pet:
	rm -rf inputs/csv/pet
	rm -rf schemas/pet
	bash download_tsv.sh pet
	ecobidas_convert --schema pet
	grep -r  "@context" schemas/pet | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/pet	

eyetracking:
	rm -rf inputs/csv/eyetracking
	rm -rf schemas/eyetracking
	bash download_tsv.sh eyetracking
	ecobidas_convert --schema eyetracking
	grep -r  "@context" schemas/eyetracking | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/eyetracking		

reexecution:
	rm -rf inputs/csv/reexecution
	rm -rf schemas/reexecution
	bash download_tsv.sh reexecution
	ecobidas_convert --schema reexecution
	grep -r  "@context" schemas/reexecution | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/reexecution	

mri:
	rm -rf inputs/csv/mri/
	rm -rf schemas/mri/
	bash download_tsv.sh core mri-
	ecobidas_convert --schema mri-allseq
	grep -r  "@context" schemas/mri | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/mri	

core:
	rm -rf inputs/csv/core/
	rm -rf schemas/core
	bash download_tsv.sh core core-
	ecobidas_convert --schema core-beh
	ecobidas_convert --schema core-participants
	grep -r  "@context" schemas/core | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/core		

# DOWNLOAD
download_all:
	bash download_tsv.sh neurovault
	bash download_tsv.sh eyetracking 
	bash download_tsv.sh pet
	bash download_tsv.sh reexecution
	bash download_tsv.sh mri-
	bash download_tsv.sh resp-
	bash download_tsv.sh core-
	bash download_tsv.sh meeg-
	bash download_subsheet_tsv.sh artemis-

download_mri:
	bash download_tsv.sh mri-

download_core: 
	bash download_tsv.sh core-	

download_meeg:
	bash download_tsv.sh meeg-

download_artemis:
	bash download_subsheet_tsv.sh artemis-

download_eyetrack:
	bash download_tsv.sh eyetracking 

download_pet:
	bash download_tsv.sh pet

download_rexec:	
	bash download_tsv.sh reexecution

download_responses:
	bash download_tsv.sh resp-

# CREATE protocol
convert_all:
	ecobidas_convert --schema pet
	ecobidas_convert --schema neurovault
	ecobidas_convert --schema eyetracking
	ecobidas_convert --schema reexecution
	ecobidas_convert --schema mri-allseq
	ecobidas_convert --schema core-participants
	ecobidas_convert --schema core-beh

# DO NOT WORK
# ecobidas_convert --schema data_sharing	
# ecobidas_convert --schema reproducibility
# ecobidas_convert --schema results
# ecobidas_convert --schema modelling_inference
# ecobidas_convert --schema preprocessing
# ecobidas_convert --schema acquisition
# ecobidas_convert --schema design

# CREATE responses

responses_all:
	ecobidas_convert --schema resp-mri_soft
	ecobidas_convert --schema resp-pres_soft
	ecobidas_convert --schema resp-multiple_comp
	ecobidas_convert --schema resp-interp
	ecobidas_convert --schema resp-cost_functions
	ecobidas_convert --schema resp-meeg_ref
	ecobidas_convert --schema resp-meeg_analysis_soft
	ecobidas_convert --schema resp-meeg_amplifier_brands
	ecobidas_convert --schema resp-meeg_acq_softwares
	ecobidas_convert --schema resp-eeg_cap_types
	ecobidas_convert --schema resp-boolean
	ecobidas_convert --schema resp-ver-spm
	ecobidas_convert --schema resp-ver-linux
	ecobidas_convert --schema resp-type-os
	ecobidas_convert --schema resp-ver-windows
	ecobidas_convert --schema resp-ver-macos
	ecobidas_convert --schema resp-eye_preproc_soft
	ecobidas_convert --schema resp-eye_model
	ecobidas_convert --schema resp-eye_producer

# VALIDATE
validate_all:
	grep -r  "@context" schemas | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas

validate_artemis:
	grep -r  "@context" schemas/artemis | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/artemis

validate_neurovault:
	grep -r  "@context" schemas/neurovault | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/neurovault

validate_responses:
	grep -r  "@context" schemas/response_options| cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/response_options

# CLEAN

clean_tsv: 
	rm -f inputs/*/*.tsv

clean_artemis:
	rm -rf inputs/csv/artemis
	rm -rf schemas/artemis/activities
clean_neurovault:
	rm -rf inputs/csv/neurovault
	rm -rf schemas/neurovault/

clean_pet:
	rm -rf schemas/pet*/

clean_mri:
	rm -rf schemas/mri*/

clean_eyetracker:
	rm -rf schemas/eye*/

clean_tests: 
	rm -rf python/*/tests/outputs	

clean_activities: 
	rm -rf schemas/*/activities