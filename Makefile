# Makefile to create the activities and protocols

.PHONY: all clean clean_protocol clean_activities clean_csv

# CREATE
neurovault:
	ecobidas_convert --schema_to_create neurovault

# DOWNLOAD
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
	sh download_tsv.sh nimg_reexecution nimg_reexecution
	sh download_tsv.sh response_options	mri_softwares	

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

# download_artemis:
#  sh download_tsv.sh artem-is artem-is

download_eyetrack:
	sh download_tsv.sh eyetracking eyetracking

download_pet:
	sh download_tsv.sh pet pet

download_rexec:	
	sh download_tsv.sh nimg_reexecution nimg_reexecution

download_responses:
	sh download_tsv.sh response_options	mri_softwares		

# CLEAN
clean_csv: 
	rm -f inputs/*.csv

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

clean_protocols: 
	rm -rf protocols/**
	rm -rf protocols/*eye*
	rm -rf protocols/*mri*
	rm -rf protocols/*neuro*
	rm -rf protocols/*pet*

clean:
	rm -rf activities/**
	rm -rf protocols/**
	rm -rf activities/*eye*
	rm -rf protocols/*eye*
	rm -rf activities/*mri*
	rm -rf protocols/*mri*
	rm -rf activities/*neuro*
	rm -rf protocols/*neuro*
	rm -rf activities/*pet*
	rm -rf protocols/*pet*