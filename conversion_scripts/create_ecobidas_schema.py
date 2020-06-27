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

# where the metadata from neurovault are described. It is in xlsx dir of this repos
# but it can also be downloaded from here:
# https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv
INPUT_FILE = '/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv'

# where the files will be written on your machine: the local repository
# corresponding to the remote where of the reproschema will be hosted
OUTPUT_DIR = '/home/remi/github/COBIDAS_chckls'

# Placeholder to insert in all instances of the remote repo that will host the schema representation
# Most likely you just need to replace Remi-Gau in the following line by your github username
REMOTE_REPO = 'https://raw.githubusercontent.com/Remi-Gau/COBIDAS_chckls/'

# to which branch of reproschema the user interface will be pointed to
# In the end the cobidas-UI repository will be reading the schema from the URL that that
# starts with: REMOTE_REPO + BRANCH
BRANCH = 'neurovault'

REPRONIM_REPO = 'https://raw.githubusercontent.com/ReproNim/reproschema/master/'


## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------
## -----------------------------------------------------------------------------

# activity set names
PROTOCOL = 'neurovault_'

# CSV column
SECTION_COL = 1
ITEM_COL = 2
QUESTION_COL = 3
RESPONSE_TYPE_COL = 4
CHOICE_COL = 5
MANDATORY_COL = 6
VISIBILITY_COL = 7

# protocol names
PROTOCOL_SCHEMA_FILE = PROTOCOL + 'schema'
PROTOCOL_CONTEXT_FILE = PROTOCOL +  'context'
PROTOCOL_DIR = PROTOCOL[0:-1]

# VERSION
VERSION = '0.0.1'

# make output directories
if not os.path.exists(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR)):
    os.makedirs(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR))


# define the jsonld for the schema protocol
PROTOCOL_SCHEMA_JSON = {
    '@context': [REPRONIM_REPO + 'contexts/generic',
                 REMOTE_REPO + BRANCH + '/protocols/'
                 + PROTOCOL_DIR + '/'
                 + PROTOCOL_CONTEXT_FILE
                ],
    '@type': 'reproschema:Protocol',
    '@id': PROTOCOL_SCHEMA_FILE,
    'prefLabel': PROTOCOL_SCHEMA_FILE,
    'schema:description': PROTOCOL_SCHEMA_FILE,
    'schema:schemaVersion': VERSION,
    'schema:version': VERSION,
    'landingPage': REMOTE_REPO + BRANCH + '/protocols/'+ PROTOCOL[0:-1] +'/README.md',
    'ui': {
        'allow': ["autoAdvance", "allowExport"],
        'shuffle': False,
        'order': [],
        'addProperties': [],
    }
}

# define the jsonld for the context associated to this protocol
PROTOCOL_CONTEXT_JSON = {
    '@context': {
        '@version': 1.1,
        'activity_path': REMOTE_REPO + BRANCH + '/activities/',
    }
}



def define_activity_context(REPRONIM_REPO, REMOTE_REPO, BRANCH, activity_dir, activity_context_file):

    context = {
        '@context': {
            '@version': 1.1,
            'item_path': REMOTE_REPO + BRANCH + '/activities/'
                         + activity_dir + '/items/',
            }
        }

    at_context = [REPRONIM_REPO + 'contexts/generic',
                 REMOTE_REPO + BRANCH + '/activities/'
                 + activity_dir + '/'
                 + activity_context_file
                ]

    return context, at_context



def define_new_activity(at_context, activity_schema_name, PROTOCOL, SECTION, VERSION):

    # define the base json content for the activity:

    return {
        '@context': at_context,
        '@type': 'reproschema:Activity',
        '@id': activity_schema_name,
        'skos:prefLabel': PROTOCOL + SECTION,
        'schema:description': PROTOCOL + SECTION,
        'schema:schemaVersion': VERSION,
        'schema:version': VERSION,
        'preamble': ' ',
        'ui': {
            'order': [],
            'shuffle': False,
            'allow': ["skipped"],
            'addProperties': [],
        }
    }



def define_new_item(at_context, item_name, question, VERSION):

    # define jsonld for this item

    return {
        '@context': at_context,
        '@type': 'reproschema:Field',
        '@id': item_name,
        'prefLabel': item_name,
        'schema:description': item_name,
        'schema:schemaVersion': VERSION,
        'schema:version': VERSION,
        'ui': {},
        'question': {
            'en': question
            },
    }



SECTION = ''
# loop through rows of the csv file and create corresponding jsonld for each item
with open(INPUT_FILE, 'r') as csvfile:
    PROTOCOL_METADATA = csv.reader(csvfile)
    for row in PROTOCOL_METADATA:

        # to skip the header
        if row[ITEM_COL] != 'Item':

            item_name = row[ITEM_COL]

            question = row[QUESTION_COL]

            response_type = row[RESPONSE_TYPE_COL]

            response_choices = row[CHOICE_COL].split('|')

            # branchic logic: visibility
            if row[VISIBILITY_COL] == '1':

                visibility = True

            else:

                visibility = row[VISIBILITY_COL]

                # vis_conditions = row[CHOICE_COL].split(',')
                #
                # for i, cdt in enumerate(vis_conditions):
                #
                #     visibility['choices'].append({
                #         'schema:name': opt,
                #         'schema:value': i,
                #         '@type': 'schema:option'
                #         })






            # detect if this is a new SECTION if so it will create a new activity
            if row[SECTION_COL] != SECTION:

                # update SECTION name
                SECTION = row[SECTION_COL]

                # where the items of this SECTION will be stored
                activity_dir = PROTOCOL + SECTION

                # names of this SECTION schema and its corresponding jsonld files
                activity_schema_name = PROTOCOL + SECTION

                activity_schema_file = activity_schema_name + '_schema'

                activity_context_file = PROTOCOL + SECTION + '_context'


                print(activity_schema_name)


                # create dir for this SECTION
                if not os.path.exists(os.path.join(OUTPUT_DIR, 'activities',
                                                   activity_dir)):
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities', activity_dir))

                if not os.path.exists(os.path.join(OUTPUT_DIR, 'activities',
                                                   activity_dir, 'items')):
                    os.makedirs(os.path.join(OUTPUT_DIR, 'activities',
                                             activity_dir, 'items'))

                activity_context_json, activity_at_context = define_activity_context(REPRONIM_REPO,
                                                                REMOTE_REPO,
                                                                BRANCH, activity_dir,
                                                                activity_context_file)

                activity_schema_json = define_new_activity(activity_at_context,
                                            activity_schema_name,
                                            PROTOCOL, SECTION, VERSION)


                # update the content of the protool schema and context wrt this new activity
                append_to_protocol = {
                    'variableName': activity_schema_name,
                    'isAbout': activity_schema_name,
                    "prefLabel": {
                    "en": activity_schema_name.replace("_"," ")
                    }
                }

                PROTOCOL_SCHEMA_JSON['ui']['order'].append(activity_schema_name)
                PROTOCOL_SCHEMA_JSON['ui']['addProperties'].append(append_to_protocol)

                PROTOCOL_CONTEXT_JSON['@context'][activity_schema_name] = {
                    '@id': 'activity_path:' + activity_dir + '/' + activity_schema_file,
                    '@type': '@id'
                    }


            print('   ' + item_name)


            # update the json content of the activity schema and context wrt this new item

            append_to_activity = {
                'variableName': item_name,
                'isAbout': item_name,
                "isVis": visibility
            }

            activity_schema_json['ui']['order'].append(item_name)
            activity_schema_json['ui']['addProperties'].append(append_to_activity)

            activity_context_json['@context'][item_name] = {
                '@id': 'item_path:' + item_name,
                '@type': '@id'
            }


            # save activity jsonld with every new item
            with open(os.path.join(OUTPUT_DIR, 'activities', activity_dir,
                                   activity_schema_file), 'w') as ff:
                json.dump(activity_schema_json, ff, sort_keys=False, indent=4)

            with open(os.path.join(OUTPUT_DIR, 'activities', activity_dir,
                                   activity_context_file), 'w') as ff:
                json.dump(activity_context_json, ff, sort_keys=False, indent=4)



            # Create new item
            item_schema_json = define_new_item(activity_at_context, item_name, question, VERSION)

            # now we define the answers for this item
            if response_type  == 'boolean':
                inputType = {'inputType': 'radio'}
                responseOptions = {
                    'multipleChoice': False,
                    'choices': [
                        {
                            'schema:value': 0,
                            'schema:name': 'No',
                            '@type': 'schema:option'
                        },
                        {
                            'schema:value': 1,
                            'schema:name': 'Yes',
                            '@type': 'schema:option'
                        },
                        {
                            'schema:value': 9,
                            'schema:name': 'Unknown',
                            '@type': 'schema:option'
                        }
                    ]
                }

            # if we have multiple choices
            elif response_type == 'dropdown':
                inputType = {'inputType': 'select'}

                responseOptions = {
                    'choices': []
                    }

                for i, opt in enumerate(response_choices):

                    responseOptions['choices'].append({
                        'schema:name': opt,
                        'schema:value': i,
                        '@type': 'schema:option'
                        })


            # response is some integer
            elif response_type  == 'int':
                inputType = {'inputType': 'number'}
                responseOptions = {'valueType': 'xsd:integer'}

            # response is some float
            elif response_type  == 'float':
                inputType = {'inputType': 'float'}
                responseOptions = {'valueType': 'xsd:float'}

            # input requires some typed answer
            elif response_type  == 'char':
                inputType = {'inputType': 'text'}
                responseOptions = {'type': 'xsd:string'}

            else:
                inputType = {'inputType': 'text'}
                responseOptions = {'type': 'xsd:string'}


            item_schema_json['ui'] = inputType
            item_schema_json['responseOptions'] = responseOptions


            # write item schema
            with open(os.path.join(OUTPUT_DIR, 'activities', activity_dir, 'items', row[ITEM_COL]), 'w') as ff:
                json.dump(item_schema_json, ff, sort_keys=False, indent=4)


# write activity set jsonld
with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR,
                       PROTOCOL_SCHEMA_FILE), 'w') as ff:
    json.dump(PROTOCOL_SCHEMA_JSON, ff, sort_keys=False, indent=4)

with open(os.path.join(OUTPUT_DIR, 'protocols', PROTOCOL_DIR,
                       PROTOCOL_CONTEXT_FILE), 'w') as ff:
    json.dump(PROTOCOL_CONTEXT_JSON, ff, sort_keys=False, indent=4)
