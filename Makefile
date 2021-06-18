# Makefile to create the activities and protocols

# TODO
# update the clean commands to clean the correct directories

.PHONY: all clean clean_protocol clean_activities clean_csv

# INSTALL
# TODO
# pip install -r requirements.txt
# git clone https://github.com/Remi-Gau/reproschema-py.git  ../../
# cd ../../reproschema-py
# git checkout remi_schema_creator

# DOWNLOAD and CREATE and VALIDATE

artemis:
	rm -rf inputs/csv/artemis
	rm -rf schemas/artemis/activities
	sh download_tsv_artemis.sh artemis hardware
	sh download_tsv_artemis.sh artemis acquisition
	sh download_tsv_artemis.sh artemis preprocessing
	sh download_tsv_artemis.sh artemis experimental_design_sample
	sh download_tsv_artemis.sh artemis measurements
	sh download_tsv_artemis.sh artemis channel_electrode_choice
	sh download_tsv_artemis.sh artemis visualization
	ecobidas_convert --schema artemis-hardware
	ecobidas_convert --schema artemis-design
	ecobidas_convert --schema artemis-measur
	ecobidas_convert --schema artemis-channel
	ecobidas_convert --schema artemis-vis
	ecobidas_convert --schema artemis-acquisition
	ecobidas_convert --schema artemis-preproc	
	grep -r  "@context" schemas/artemis | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/artemis

neurovault:
	rm -rf inputs/csv/neurovault
	rm -rf schemas/neurovault
	sh download_tsv.sh neurovault neurovault
	ecobidas_convert --schema neurovault
	grep -r  "@context" schemas/neurovault | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/neurovault

pet:
	rm -rf inputs/csv/pet
	rm -rf schemas/pet
	sh download_tsv.sh pet pet
	ecobidas_convert --schema pet
	grep -r  "@context" schemas/pet | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/pet	

eyetracking:
	rm -rf inputs/csv/eyetracking
	rm -rf schemas/eyetracking
	sh download_tsv.sh eyetracking eyetracking
	ecobidas_convert --schema eyetracking
	grep -r  "@context" schemas/eyetracking | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/eyetracking		

reexecution:
	rm -rf inputs/csv/reexecution
	rm -rf schemas/reexecution
	sh download_tsv.sh reexecution reexecution
	ecobidas_convert --schema reexecution
	grep -r  "@context" schemas/reexecution | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/reexecution	

all_sequences:
	rm -rf inputs/csv/core/all_sequences.tsv
	rm -rf schemas/core/activities/common_parameters
	rm -rf schemas/core/protocols/all_sequences*
	sh download_tsv.sh core all_sequences
	ecobidas_convert --schema mri-allseq
	grep -r  "@context" schemas/mri | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/mri	

behavior:
	rm -rf inputs/csv/core/behavior.tsv
	rm -rf schemas/core/activities/behavior
	rm -rf schemas/core/protocols/behavior*
	sh download_tsv.sh core behavior
	ecobidas_convert --schema core-beh
	grep -r  "@context" schemas/core | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/core

participants:
	rm -rf inputs/csv/core/participants.tsv
	rm -rf schemas/core/activities/behavior
	rm -rf schemas/core/protocols/participants*
	sh download_tsv.sh core participants
	ecobidas_convert --schema core-participants
	grep -r  "@context" schemas/core | cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/core		

# DOWNLOAD

# TODO
# simplify by making download script more powerful

ALL_MRI = $(wildcard inputs/csv/mri/*.tsv)
download_all:
	sh download_tsv.sh neurovault neurovault
	sh download_tsv.sh mri all_sequences
	sh download_tsv.sh mri design
	sh download_tsv.sh mri acquisition
	sh download_tsv.sh mri preprocessing
	sh download_tsv.sh mri modelling_inference
	sh download_tsv.sh mri results
	sh download_tsv.sh core participants
	sh download_tsv.sh core behavior
	sh download_tsv.sh core reproducibility
	sh download_tsv.sh core data_sharing	
	sh download_tsv.sh meeg design
	sh download_tsv.sh meeg acquisition
	sh download_tsv.sh meeg processing
	sh download_tsv.sh meeg statistical_analysis
	sh download_tsv.sh meeg reporting 	
	sh download_tsv.sh artem-is artem-is
	sh download_tsv.sh eyetracking eyetracking
	sh download_tsv.sh pet pet
	sh download_tsv.sh reexecution reexecution
	sh download_tsv.sh response_options	mri_softwares
	sh download_tsv.sh response_options	stimulus_presentation_softwares
	sh download_tsv.sh response_options	multiple_comparisons
	sh download_tsv.sh response_options	interpolations
	sh download_tsv.sh response_options	cost_functions
	sh download_tsv.sh response_options	meeg_reference_electrodes
	sh download_tsv.sh response_options	meeg_analysis_softwares
	sh download_tsv.sh response_options	meeg_amplifier_brands
	sh download_tsv.sh response_options	meeg_acquisition_softwares
	sh download_tsv.sh response_options	eeg_cap_types
	sh download_tsv.sh response_options	boolean

download_neurovault: 
	sh download_tsv.sh neurovault neurovault

download_mri: $(ALL_MRI)
	sh download_tsv.sh mri all_sequences
	sh download_tsv.sh mri design
	sh download_tsv.sh mri acquisition
	sh download_tsv.sh mri preprocessing
	sh download_tsv.sh mri modelling_inference
	sh download_tsv.sh mri results

download_core: 
	sh download_tsv.sh core participants
	sh download_tsv.sh core behavior
	sh download_tsv.sh core reproducibility
	sh download_tsv.sh core data_sharing	

download_meeg:
	sh download_tsv.sh meeg design
	sh download_tsv.sh meeg acquisition
	sh download_tsv.sh meeg processing
	sh download_tsv.sh meeg statistical_analysis
	sh download_tsv.sh meeg reporting 	

download_artemis:
	sh download_tsv_artemis.sh artemis hardware
	sh download_tsv_artemis.sh artemis acquisition
	sh download_tsv_artemis.sh artemis preprocessing
	sh download_tsv_artemis.sh artemis experimental_design_sample
	sh download_tsv_artemis.sh artemis measurements
	sh download_tsv_artemis.sh artemis channel_electrode_choice
	sh download_tsv_artemis.sh artemis visualization	

download_eyetrack:
	sh download_tsv.sh eyetracking eyetracking

download_pet:
	sh download_tsv.sh pet pet

download_rexec:	
	sh download_tsv.sh reexecution reexecution

download_responses:
	sh download_tsv.sh response_options	mri_softwares
	sh download_tsv.sh response_options	stimulus_presentation_softwares
	sh download_tsv.sh response_options	multiple_comparisons
	sh download_tsv.sh response_options	interpolations
	sh download_tsv.sh response_options	cost_functions
	sh download_tsv.sh response_options	meeg_reference_electrodes
	sh download_tsv.sh response_options	meeg_analysis_softwares
	sh download_tsv.sh response_options	meeg_amplifier_brands
	sh download_tsv.sh response_options	meeg_acquisition_softwares
	sh download_tsv.sh response_options	eeg_cap_types
	sh download_tsv.sh response_options	boolean
	sh download_tsv.sh response_options	spm_version
	sh download_tsv.sh response_options	linux_version
	sh download_tsv.sh response_options	type_os
	sh download_tsv.sh response_options	windows_version
	sh download_tsv.sh response_options	macos_version
	sh download_tsv.sh response_options	eyetracker_preproc_softwares
	sh download_tsv.sh response_options	eyetracker_model_name
	sh download_tsv.sh response_options	eyetracker_producer



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

validate_responses:
	grep -r  "@context" schemas/response_options| cut -d: -f1 | xargs -I fname jsonlint -q fname
	reproschema -l DEBUG validate schemas/response_options

# CLEAN

# TODO 
# use wildcards to simplify 
clean_tsv: 
	rm -f inputs/*/*.tsv

clean_artemis:
	rm -rf schemas/artemis/activities
clean_neurovault:
	rm -rf activities/*neuro*
	rm -rf protocols/*neuro*

clean_pet:
	rm -rf activities/*pet*
	rm -rf protocols/*pet*

clean_mri:
	rm -rf activities/*mri*
	rm -rf protocols/*mri*

clean_eyetracker:
	rm -rf activities/*eye*
	rm -rf protocols/*eye*

clean_tests: 
	rm -rf python/*/tests/outputs	

clean_activities: 
	rm -rf activities/**
	rm -rf activities/*eye*
	rm -rf activities/*mri*
	rm -rf activities/*neuro*
	rm -rf activities/*pet*
	rm -rf activities/*artemis*

clean_protocols: 
	rm -rf protocols/*eye*
	rm -rf protocols/*mri*
	rm -rf protocols/*neuro*
	rm -rf protocols/*pet*

clean:
	rm -rf activities/**
	rm -rf activities/*eye*
	rm -rf protocols/*eye*
	rm -rf activities/*mri*
	rm -rf protocols/*mri*
	rm -rf activities/*neuro*
	rm -rf protocols/*neuro*
	rm -rf activities/*pet*
	rm -rf protocols/*pet*