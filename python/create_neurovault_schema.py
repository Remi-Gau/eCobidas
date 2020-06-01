# this script takes the content of the metadata csv file from neurvovault and turns
# it into a Repronim compliant schema

# tested with python 3.7

import json
import os
import csv


## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
# modify the following lines to match your needs

# where the metadata from neurovault are described. It is in xlsx folder of this repos
# but it can also be downloaded from here:
# https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv
INPUT_FILE = '/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv'

# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted
OUTPUT_DIR = '/home/remi/github/reproschema'

# Placeholder to insert in all instances of the remote repo that will host the schema representation
# Most likely you just need to replace Remi-Gau in the following line by your github username
REMOTE_REPO = 'https://raw.githubusercontent.com/Remi-Gau/reproschema/'

# to which branch of reproschema the user interface will be pointed to
# In the end the cobidas-UI repository will be reading the schema from the URL that that
# starts with: REMOTE_REPO + BRANCH_NAME
BRANCH_NAME = 'eCOBIDAS'

REPRONIM_REPO = 'https://raw.githubusercontent.com/ReproNim/reproschema/master/'


## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------

# activity set names
PROTOCOL_SCHEMA_FILENAME = 'Cobidas_schema'
PROTOCOL_CONTEXT_FILENAME = 'Cobidas_context'
PROTOCOL_FOLDER_NAME = 'cobidas'


# VERSION
VERSION = '0.0.1'

# make output directories
if not os.path.exists(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_FOLDER_NAME)):
    os.makedirs(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_FOLDER_NAME))


# define the activity set neurovault_schema.jsonld
PROTOCOL_SCHEMA_JSON = {
    '@context': [REPRONIM_REPO + 'contexts/generic',
                 REMOTE_REPO + BRANCH_NAME + '/protocols/'
                 + PROTOCOL_FOLDER_NAME + '/'
                 + PROTOCOL_CONTEXT_FILENAME
                ],
    '@type': 'reproschema:ActivitySet',
    '@id': 'cobidas_schema',
    'skos:prefLabel': 'eCOBIDAS proof of concept',
    'skos:altLabel': 'eCOBIDAS_POC',
    'schema:description': 'neurovault as a COBIDAS checklist proof of concept',
    'schema:schemaVersion': VERSION,
    'schema:version': VERSION,
    'about': REMOTE_REPO + BRANCH_NAME + '/protocols/README.md',
    'variableMap': [],
    'ui': {
        'order': [],
        'shuffle': False,
        'activity_display_name': {},
        'visibility': {}
    }
}

# define the activity set neurovault_context.jsonld
PROTOCOL_CONTEXT_JSON = {
    '@context': {
        '@version': 1.1,
        'activity_path': REMOTE_REPO + BRANCH_NAME + '/activities/',
    }
}


SECTION = ''
# loop through rows of the csv file and create corresponding jsonld for each item
with open(INPUT_FILE, 'r') as csvfile:
    PROTOCOL_METADATA = csv.reader(csvfile)
    for row in PROTOCOL_METADATA:

        # to skip the header
        if row[2] != 'Item':

            # detect if this is a new SECTION if so it will create a new activity
            if row[1] != SECTION:

                # update SECTION name
                SECTION = row[1]

                # where the items of this SECTION will be stored
                activity_folder_name = 'Cobidas' + SECTION

                # names of this SECTION schema and its corresponding jsonld files
                activity_schema_name = 'Cobidas' + SECTION + '_schema'

                activity_schema_filename = activity_schema_name

                activity_context_filename = 'Cobidas' + SECTION + '_context'


                print(activity_schema_name)

                # create dir for this SECTION
                if not os.path.exists(os.path.join(OUTPUT_DIR, 'activities',
                                                   activity_folder_name)):
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities', activity_folder_name))

                if not os.path.exists(os.path.join(OUTPUT_DIR, 'activities',
                                                   activity_folder_name, 'items')):
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities',
                                             activity_folder_name, 'items'))


                # define the base json content for the activity:
                # neurovault_schema.jsonld
                # neurovault_context.jsonld
                protocol_context_json = {
                    '@context': {
                        '@version': 1.1,
                        'item_path': REMOTE_REPO + BRANCH_NAME + '/activities/'
                                     + activity_folder_name + '/items/',
                        }
                    }

                protocol_schema_json = {
                    '@context': [REPRONIM_REPO + 'contexts/generic',
                                 REMOTE_REPO + BRANCH_NAME + '/activities/'
                                 + activity_folder_name + '/'
                                 + activity_context_filename
                                ],
                    '@type': 'reproschema:Activity',
                    '@id': activity_schema_name,
                    'skos:prefLabel': 'Cobidas' + SECTION,
                    'skos:altLabel': 'Cobidas' + SECTION,
                    'schema:description': 'Cobidas' + SECTION,
                    'schema:schemaVersion': VERSION,
                    'schema:version': VERSION,
                    'variableMap': [],
                    'preamble': ' ',
                    'ui': {
                        'order': [],
                        'visibility': {},
                        'shuffle': False,
                        'allow': ["skipped"]
                    }
                }

                # update the json content of activity set schema and context wrt this new activity
                PROTOCOL_SCHEMA_JSON['variableMap'].append(
                    {'variableName': activity_schema_name, 'isAbout': activity_schema_name}
                    )

                PROTOCOL_SCHEMA_JSON['ui']['order'].append(activity_schema_name)
                PROTOCOL_SCHEMA_JSON['ui']['visibility'][activity_schema_name] = True
                PROTOCOL_SCHEMA_JSON['ui']['activity_display_name'][activity_schema_name] = SECTION + '_schema' # TO DO: add space when upercase

                PROTOCOL_CONTEXT_JSON['@context'][activity_schema_name] = {
                    '@id': 'activity_path:' + activity_folder_name + '/' + activity_schema_filename,
                    '@type': '@id'
                    }

            print('   ' + row[2])


            # update the json content of the activity schema and context wrt this new item
            protocol_context_json['@context'][row[2]] = {
                '@id': 'item_path:' + row[2],
                '@type': '@id'
            }

            protocol_schema_json['ui']['order'].append(row[2])

            protocol_schema_json['variableMap'].append(
                {'variableName': row[2], 'isAbout': row[2]}
                )

            # branchic logic: visibility
            if row[6] == '1':
                protocol_schema_json['ui']['visibility'][row[2]] = True
            else:
                protocol_schema_json['ui']['visibility'][row[2]] = row[6] + ' === 1'



            # save activity jsonld with every new item
            with open(os.path.join(OUTPUT_DIR, 'activities', activity_folder_name,
                                   activity_schema_filename), 'w') as ff:
                json.dump(protocol_schema_json, ff, sort_keys=False, indent=4)

            with open(os.path.join(OUTPUT_DIR, 'activities', activity_folder_name,
                                   activity_context_filename), 'w') as ff:
                json.dump(protocol_context_json, ff, sort_keys=False, indent=4)


            # define jsonld for this item
            item_json = {
                '@context': [REPRONIM_REPO + 'contexts/generic',
                             REMOTE_REPO + BRANCH_NAME + '/activities/'
                             + activity_folder_name + '/'
                             + activity_context_filename
                            ],
                '@type': 'reproschema:Field',
                '@id': row[2],
                'skos:prefLabel': row[2],
                'skos:altLabel': row[2],
                'schema:description': row[2],
                'schema:schemaVersion': VERSION,
                'schema:version': VERSION,
                'question': row[3],
            }

            # now we define the answers for this item
            if row[4] == 'Boolean':

                item_json['ui'] = {
                    'inputType': 'radio'
                }
                item_json['responseOptions'] = {
                    '@type': 'xsd:anyURI',
                    'multipleChoice': False,
                    'minValue': 0,
                    'maxValue': 1,
                    'choices': [
                        {
                            '@type': 'Boolean',
                            'name': 'no',
                            'value': 0,
                        },
                        {
                            '@type': 'Boolean',
                            'name': 'yes',
                            'value': 1,
                        }
                    ]
                }

            # if we have multiple choices
            elif row[4][0] == '[':

                # we get all the possible options and add them to the possible responses
                options = row[4][1:-2].replace("'", "").split(',')

                item_json['ui'] = {
                    'inputType': 'select'
                    }

                item_json['responseOptions'] = {
                    "dataType": "xsd:string",
                    'multipleChoice': True,
                    'minValue': 0,
                    'maxValue': len(options)-1,
                    'choices': []
                    }

                for i, opt in enumerate(options):

                    item_json['responseOptions']['choices'].append({
                        'name': {'en': opt},
                        'value': i,
                        })


            # response is some integer
            elif row[4] == 'int':
                item_json['ui'] = {
                    'inputType': 'number'
                }
                item_json['responseOptions'] = {
                    'type': 'xsd:integer',
                }


            # response is some float
            elif row[4] == 'float':
                item_json['ui'] = {
                    'inputType': 'float'
                }
                item_json['responseOptions'] = {
                    'type': 'xsd:float',
                }


            # input requires some typed answer
            elif row[4] == 'char':
                item_json['ui'] = {
                    'inputType': 'text'
                    }
                item_json['responseOptions'] = {
                    'type': 'xsd:string'
                    }

            else:
                item_json['ui'] = {
                    'inputType': 'text'
                    }
                item_json['responseOptions'] = {
                    'type': 'xsd:string'
                    }


            # write item jsonld
            with open(os.path.join(OUTPUT_DIR, 'activities', activity_folder_name, 'items', row[2]), 'w') as ff:
                json.dump(item_json, ff, sort_keys=False, indent=4)


# write activity set jsonld
with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_FOLDER_NAME,
                       PROTOCOL_SCHEMA_FILENAME), 'w') as ff:
    json.dump(PROTOCOL_SCHEMA_JSON, ff, sort_keys=False, indent=4)

with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_FOLDER_NAME,
                       PROTOCOL_CONTEXT_FILENAME), 'w') as ff:
    json.dump(PROTOCOL_CONTEXT_JSON, ff, sort_keys=False, indent=4)
