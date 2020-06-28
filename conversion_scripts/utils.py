def define_activity_context(REPRONIM_REPO, REMOTE_REPO, BRANCH, activity_dir, activity_context_file):

    context = {
        '@context': {
            '@version': 1.1,
            'item_path': REMOTE_REPO + BRANCH + '/activities/'
            + activity_dir + '/items/'
            }
        }

    at_context = [
        REPRONIM_REPO + 'contexts/generic',
        REMOTE_REPO + BRANCH + '/activities/'
        + activity_dir + '/'
        + activity_context_file
        ]

    return context, at_context


def define_new_activity(at_context, activity_schema_name, PROTOCOL, section, VERSION):
    # define the base json content for the activity
    return {
        '@context': at_context,
        '@type': 'reproschema:Activity',
        '@id': activity_schema_name,
        'skos:prefLabel': PROTOCOL + section,
        'schema:description': PROTOCOL + section,
        'schema:schemaVersion': VERSION,
        'schema:version': VERSION,
        'preamble': ' ',
        'ui': {
            'order': [],
            'shuffle': False,
            'allow': ["skipped"],
            'addProperties': []
            }
        }


def get_item_info(row, ITEM_COL, QUESTION_COL, RESPONSE_TYPE_COL, CHOICE_COL, VISIBILITY_COL, INCLUDE_COL):

    item_name = []
    question = "QUESTION MISSING"
    response_type = "UNKNOWN"
    response_choices = []
    visibility = True

    INCLUDE = True
    # we want to skip the header and only include items with 1 in the include column (if it exists)
    if row[ITEM_COL] == 'Item' or (INCLUDE_COL != [] and row[INCLUDE_COL] != "1"):
        INCLUDE = False

        print('   skipping item')

    if INCLUDE:

        item_name = row[ITEM_COL].replace("\n", "")

        question = row[QUESTION_COL].replace("\n", "")

        response_type = row[RESPONSE_TYPE_COL]

        response_choices = row[CHOICE_COL].split(' | ')

        # branchic logic: visibility
        if row[VISIBILITY_COL] != '1':

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

    return item_name, question, response_type, response_choices, visibility


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
        'ui': {
            'allow': ["skipped"],
            'inputType': []
        },
        'question': {
            'en': question
            },
        }


def define_response_choice(response_type, response_choices):
    # now we define the answers for this item
    if response_type == 'boolean':

        inputType = 'radio'

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

    # if we have multiple choices with a radio item
    elif response_type == 'radio':

        inputType = 'radio'

        responseOptions = {'choices': []}

        responseOptions = list_responses_options(responseOptions, response_choices)

    # if we have a dropdown menu
    elif response_type == 'dropdown':

        inputType = 'select'

        responseOptions = {'choices': []}

        responseOptions = list_responses_options(responseOptions, response_choices)

    # response is date
    elif response_type == 'date':
        inputType = 'date'
        responseOptions = {'valueType': 'xsd:date'}

    # response is time range
    elif response_type == 'time range':
        inputType = 'timeRange'
        responseOptions = {'valueType': 'datetime'}

    # response is slider
    elif response_type == 'slider':
        inputType = 'slider'
        responseOptions = {
            'valueType': 'xsd:integer',
            'schema:minValue': 0,
            'schema:maxValue': 6,
            'choices': [
                {
                    'schema:name': 'Not at all',
                    'schema:value': 0,
                    '@type': 'schema:option'
                },
                {
                    'schema:value': 1,
                    '@type': 'schema:option'
                },
                {
                    'schema:value': 2,
                    '@type': 'schema:option'
                },
                {
                    'schema:value': 3,
                    '@type': 'schema:option'
                },
                {
                    'schema:value': 4,
                    '@type': 'schema:option'
                },
                {
                    'schema:value': 5,
                    '@type': 'schema:option'
                },
                {
                    'schema:name': 'Completely',
                    'schema:value': 6,
                    '@type': 'schema:option'
                }
            ]
        }

    # response is integer
    elif response_type == 'int':
        inputType = 'number'
        responseOptions = {'valueType': 'xsd:integer'}

    # response is float
    elif response_type == 'float':
        inputType = 'float'
        responseOptions = {'valueType': 'xsd:float'}

    # input requires typed answer
    elif response_type == 'char':
        inputType = 'text'
        responseOptions = {'type': 'xsd:string'}

    else:
        inputType = 'text'
        responseOptions = {'type': 'xsd:string'}

    return inputType, responseOptions


def list_responses_options(responseOptions, response_choices):

    for i, opt in enumerate(response_choices):

        responseOptions['choices'].append({
            'schema:name': opt,
            'schema:value': i,
            '@type': 'schema:option'
            }
        )

    responseOptions['choices'].append({
            'schema:name': 'Other',
            'schema:value': len(response_choices) + 1,
            '@type': 'schema:option'
            }
        )

    return responseOptions