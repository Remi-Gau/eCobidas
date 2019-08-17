# this script takes the content of the metadata csv file from neurvovault and turns
# it into a Repronim compliant schema

# tested with python 3.7

import json
import os
import csv

# where the metadata from neurovault are described. Can be downloaded from here:v
# https://github.com/NeuroVault/NeuroVault/blob/master/scripts/metadata_neurovault.csv
input_file = '/home/remi/github/COBIDAS_chckls/xlsx/metadata_neurovault.csv'

# where the files will be written (the local repo of the schema-standardization)
output_dir = '/home/remi/github/schema-standardization'

# placeholder to insert in all instances of the remote repo
remote_repo = 'https://raw.githubusercontent.com/Remi-Gau/schema-standardization/'

# to which branch of schema-standardization the ui will be pointed to
branch_name  = 'neurovault'


# activity set names
activity_set_schema_filename = 'cobidas_schema.jsonld'
activity_set_context_filename = 'cobidas_context.jsonld'
activity_set_folder_name = 'cobidas'


# version
version = '0.0.1'

# make output directories
if not os.path.exists(os.path.join(output_dir, 'activity-sets', activity_set_folder_name)):
    os.makedirs(os.path.join(output_dir, 'activity-sets', activity_set_folder_name))



# define the activity set neurovault_schema.jsonld
nv_set_schema_json = {
    '@context': [ remote_repo + branch_name + '/contexts/generic.jsonld',
        remote_repo + branch_name + '/activity-sets/' + activity_set_folder_name + '/' + activity_set_context_filename
    ],
    '@type': remote_repo + branch_name + '/schemas/ActivitySet.jsonld',
    '@id': 'cobidas_schema',
    'skos:prefLabel': 'neurovault as a COBIDAS POC',
    'skos:altLabel': 'neurovault_COBIDAS_POC',
    'schema:description': 'neurovault as a COBIDAS checklist proof of concept',
    'schema:schemaVersion': version,
    'schema:version': version,
    'variableMap': [],
    'ui': {
        'order': [],
        'shuffle': False,
        'activity_display_name': {},
        'visibility': {}
    }
}

# define the activity set neurovault_context.jsonld
nv_set_context_json = {
    '@context': {
        '@version': 1.1,
        'activity_path': remote_repo + branch_name + '/activities/',
    }
}


Section = ''
# loop through rows of the csv file and create corresponding jsonld for each item
with open(input_file, 'r') as csvfile:
    nv_metadata = csv.reader(csvfile)
    for row in nv_metadata:

        # to skip the header
        if row[2]!='Item':

            # detect if this is a new section if so it will create a new activity
            if row[1]!=Section:

                # update section name
                Section=row[1]

                # where the items of this section will be stored
                activity_folder_name = 'Neurovault_' + Section

                # names of this section schema and its corresponding jsonld files
                activity_schema_name = 'Neurovault_' + Section + '_schema'

                activity_schema_filename = activity_schema_name + '.jsonld'

                activity_context_filename = 'Neurovault_' + Section + '_context.jsonld'


                print(activity_schema_name)

                # create dir for this section
                if not os.path.exists(os.path.join(output_dir, 'activities', activity_folder_name)):
                    os.makedirs(os.path.join(output_dir, 'activities', activity_folder_name))

                if not os.path.exists(os.path.join(output_dir, 'activities', activity_folder_name, 'items')):
                    os.makedirs(os.path.join(output_dir, 'activities', activity_folder_name, 'items'))


                # define the base json content for the activity: neurovault_schema.jsonld neurovault_context.jsonld
                nv_context_json = {
                    '@context': {
                        '@version': 1.1,
                        'item_path': remote_repo + branch_name + '/activities/' + activity_folder_name + '/items/',
                        }
                    }

                nv_schema_json = {
                    '@context': [ remote_repo + branch_name + '/contexts/generic.jsonld',
                        remote_repo + branch_name + '/activities/' + activity_folder_name + '/' + activity_context_filename
                    ],
                    '@type': remote_repo + branch_name + '/schemas/Activity.jsonld',
                    '@id': activity_schema_name,
                    'skos:prefLabel': 'COBIDAS design checklist',
                    'skos:altLabel': 'cobidas_design_schema',
                    'schema:description': 'COBIDAS design checklist schema',
                    'schema:schemaVersion': version,
                    'schema:version': version,
                    'preamble': 'How did you design/analyse your study?',
                    'ui': {
                        'order': [],
                        'shuffle': False
                    }
                }

                # update the json content of the activity set schema and context wrt this new activity
                nv_set_schema_json['variableMap'].append(
                    {'variableName': activity_schema_name,'isAbout': activity_schema_name}
                    )

                nv_set_schema_json['ui']['order'].append(activity_schema_name)
                nv_set_schema_json['ui']['visibility'][activity_schema_name] = True
                nv_set_schema_json['ui']['activity_display_name'][activity_schema_name] = 'Neurovault - ' + Section

                nv_set_context_json['@context'][activity_schema_name] = {
                    '@id': 'activity_path:' + activity_folder_name + '/' + activity_schema_filename,
                    '@type': '@id'
                    }

            print('   ' + row[2])


            # update the json content of the activity schema and context wrt this new item
            nv_schema_json['ui']['order'].append(row[2])

            nv_context_json['@context'][row[2]] = {
                '@id': 'item_path:'+row[2]+'.jsonld',
                '@type': '@id'
            }

            # save activity jsonld with every new item
            with open(os.path.join(output_dir, 'activities', activity_folder_name, activity_schema_filename), 'w') as ff:
                json.dump(nv_schema_json, ff, sort_keys=False, indent=4)

            with open(os.path.join(output_dir, 'activities', activity_folder_name, activity_context_filename), 'w') as ff:
                json.dump(nv_context_json, ff, sort_keys=False, indent=4)


            # define jsonld for this item
            item_json = {
                '@context': [ remote_repo + branch_name + '/contexts/generic.jsonld',
                    remote_repo + branch_name + '/activities/' + activity_folder_name + '/' + activity_context_filename
                ],
                '@type': remote_repo + branch_name + '/schemas/Field.jsonld',
                '@id': row[2],
                'skos:prefLabel': row[2],
                'skos:altLabel': row[2],
                'schema:description': row[2],
                'schema:schemaVersion': version,
                'schema:version': version,
                'question': row[3],
            }

            # now we define the answers for this item
            if row[4]=='Boolean':

                item_json['ui'] = {
                    'inputType': 'radio'
                }
                item_json['responseOptions'] = {
                    '@type': 'xsd:anyURI',
                    'multipleChoice': False,
                    'schema:minValue': 0,
                    'schema:maxValue': 1,
                    'choices': [
                        {
                        '@type': 'schema:Boolean',
                        'schema:name': 'no',
                        'schema:value': 0,
                        },
                        {
                        '@type': 'schema:Boolean',
                        'schema:name': 'yes',
                        'schema:value': 1,
                        }
                    ]
                }

            # if we have multiple choices
            elif row[4][0]=='[':

                # we get all the possible options and add them to the possible responses
                options = row[4][1:-2].replace("'", "").split(',')

                item_json['ui'] = {
                    'inputType': 'radio'
                    }

                item_json['responseOptions'] = {
                    '@type': 'xsd:anyURI',
                    'multipleChoice': False,
                    'schema:minValue': 0,
                    'schema:maxValue': len(options)-1,
                    'choices': []
                    }

                for i, opt in enumerate(options):

                    item_json['responseOptions']['choices'].append({
                            'schema:name': {'en': opt},
                            'schema:value': i,
                            })


            # response is some integer
            elif row[4]=='int':
                    item_json['ui'] = {
                        'inputType': 'text'
                    }
                    item_json['responseOptions'] = {
                        'type': 'xsd:int',
                    }


            # response is some integer
            elif row[4]=='float':
                        item_json['ui'] = {
                            'inputType': 'text'
                        }
                        item_json['responseOptions'] = {
                            'type': 'xsd:float',
                        }


            # input requires some typed answer
            elif row[4]=='char':
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
            with open(os.path.join(output_dir, 'activities', activity_folder_name, 'items', row[2] + '.jsonld'), 'w') as ff:
                json.dump(item_json, ff, sort_keys=False, indent=4)


# write activity set jsonld
with open(os.path.join(output_dir, 'activity-sets', activity_set_folder_name, activity_set_schema_filename), 'w') as ff:
    json.dump(nv_set_schema_json, ff, sort_keys=False, indent=4)

with open(os.path.join(output_dir, 'activity-sets', activity_set_folder_name, activity_set_context_filename), 'w') as ff:
    json.dump(nv_set_context_json, ff, sort_keys=False, indent=4)
