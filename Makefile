# Makefile to create the activitie and protocols

# INPUT_DIR = $(inputs/csv/)
# OUTPUT_DIR = $(inputs/csv/)

# ALL_CSV = $(wildcard $(INPUT_DIR)cobidas_*.csv)
# ALL_CSV = $(wildcard data/*.csv)
# INPUT_CSV = $(wildcard data/input_file_*.csv)
# DATA = $(filter-out $(INPUT_CSV),$(ALL_CSV))
# FIGURES = $(patsubst data/%.csv,output/figure_%.png,$(DATA))

.PHONY: all clean clean_protocol clean_activities clean_csv

all: inputs/csv/cobidas_%.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema.py -i $< -o $@

protocols/cobidas_neurovault/cobidas_neurovault_schema: inputs/csv/cobidas_neurovault.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema("neurovault") -i $< -o $@

protocols/cobidas_mri/cobidas_mri_schema: inputs/csv/cobidas_mri.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema.py -i $< -o $@

protocols/cobidas_pet/cobidas_pet_schema: inputs/csv/cobidas_pet.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema.py -i $< -o $@

protocols/cobidas_pet/cobidas_eyetracker_schema: inputs/csv/cobidas_eyetracker.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema.py -i $< -o $@

protocols/cobidas_pet/cobidas_meeg_schema: inputs/csv/cobidas_meeg.csv scripts/create_ecobidas_schema.py
	python scripts/create_ecobidas_schema.py -i $< -o $@


clean_csv: 
	rm -f inputs/cobidas_*.csv

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

clean_activities: 
	rm -rf activities/*cobidas_*
	rm -rf activities/*eye*
	rm -rf activities/*mri*
	rm -rf activities/*neuro*
	rm -rf activities/*pet*

clean_protocols: 
	rm -rf protocols/*cobidas_*
	rm -rf protocols/*eye*
	rm -rf protocols/*mri*
	rm -rf protocols/*neuro*
	rm -rf protocols/*pet*

clean:
	rm -rf activities/*cobidas_*
	rm -rf protocols/*cobidas_*
	rm -rf activities/*eye*
	rm -rf protocols/*eye*
	rm -rf activities/*mri*
	rm -rf protocols/*mri*
	rm -rf activities/*neuro*
	rm -rf protocols/*neuro*
	rm -rf activities/*pet*
	rm -rf protocols/*pet*