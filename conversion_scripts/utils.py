def define_new_protocol(REPRONIM_REPO, REMOTE_REPO, BRANCH, protocol, VERSION):

    # protocol names
    protocol["schema_file"] = protocol["name"] + "schema"
    protocol["context_file"] = protocol["name"] + "context"
    protocol["dir"] = protocol["name"][0:-1]

    # define the jsonld for the schema protocol
    protocol["schema"] = {
        "@context": [
            REPRONIM_REPO + "contexts/generic",
            REMOTE_REPO
            + BRANCH
            + "/protocols/"
            + protocol["dir"]
            + "/"
            + protocol["context_file"],
        ],
        "@type": "reproschema:Protocol",
        "@id": protocol["schema_file"],
        "prefLabel": protocol["schema_file"],
        "schema:description": protocol["schema_file"],
        "schema:schemaVersion": VERSION,
        "schema:version": VERSION,
        "landingPage": REMOTE_REPO
        + BRANCH
        + "/protocols/"
        + protocol["dir"]
        + "/README.md",
        "ui": {
            "allow": ["autoAdvance", "allowExport"],
            "shuffle": False,
            "order": [],
            "addProperties": [],
        },
    }

    # define the jsonld for the context associated to this protocol
    protocol["context"] = {
        "@context": {
            "@version": 1.1,
            "activity_path": REMOTE_REPO + BRANCH + "/activities/",
        }
    }

    return protocol


def define_activity_context(
    REPRONIM_REPO, REMOTE_REPO, BRANCH, activity_dir, activity_context_file
):
    # """Validate a directory containing JSONLD documents

    # .. warning:: This assumes every file in the directory can be read by a json parser.

    # Parameters
    # ----------
    # directory: str
    #     Path to directory to walk for validation
    # shape_dir: str
    #     Path containing validation SHACL shape files
    # started : bool
    #     Whether an http server exists or not
    # http_kwargs : dict
    #     Keyword arguments for the http server. Valid keywords are: port, path
    #     and tmpdir

    # Returns
    # -------
    # conforms: bool
    #     Whether the document is conformant with the shape. Raises an exception
    #     if any document is non-conformant.

    # """
    context = {
        "@context": {
            "@version": 1.1,
            "item_path": REMOTE_REPO
            + BRANCH
            + "/activities/"
            + activity_dir
            + "/items/",
        }
    }

    at_context = [
        REPRONIM_REPO + "contexts/generic",
        REMOTE_REPO
        + BRANCH
        + "/activities/"
        + activity_dir
        + "/"
        + activity_context_file,
    ]

    return at_context, context


def define_new_activity(at_context, activity_schema_file, protocol, section, VERSION):
    # define the base json content for the activity
    return {
        "@context": at_context,
        "@type": "reproschema:Activity",
        "@id": activity_schema_file,
        "skos:prefLabel": protocol + section,
        "schema:description": protocol + section,
        "schema:schemaVersion": VERSION,
        "schema:version": VERSION,
        "preamble": " ",
        "ui": {
            "order": [],
            "shuffle": False,
            "allow": ["skipped"],
            "addProperties": [],
        },
    }


def get_item_info(row, CSV_INFO):

    mandatory_col = CSV_INFO["mandatory"]["col"]

    item_name = []
    question = "QUESTION MISSING"
    response_type = "UNKNOWN"
    response_choices = []
    visibility = True

    item_col = CSV_INFO["item"]["col"]
    item_col_name = CSV_INFO["item"]["name"]

    # we want to skip the header and only include items with 1 in the include column (if it exists)
    INCLUDE = True
    incl_col = CSV_INFO["include"]["col"]
    if row[item_col] == item_col_name or (incl_col != [] and row[incl_col] != "1"):

        INCLUDE = False

        print("   skipping item")

        return {"name": item_name}

    if INCLUDE:

        item_name = row[item_col].replace("\n", "")

        question_col = CSV_INFO["question"]["col"]
        question = row[question_col].replace("\n", "")

        resp_type_col = CSV_INFO["resp_type"]["col"]
        response_type = row[resp_type_col]

        choice_col = CSV_INFO["choice"]["col"]
        response_choices = row[choice_col].split(" | ")

        vis_col = CSV_INFO["vis"]["col"]

        # branchic logic: visibility
        if row[vis_col] != "1":

            visibility = row[vis_col]

            # vis_conditions = row[choice_col].split(',')
            #
            # for i, cdt in enumerate(vis_conditions):
            #
            #     visibility['choices'].append({
            #         'schema:name': opt,
            #         'schema:value': i,
            #         '@type': 'schema:option'
            #         })

    return {
        "name": item_name,
        "question": question,
        "resp_type": response_type,
        "choices": response_choices,
        "visibility": visibility,
    }


def define_new_item(at_context, item_name, question, VERSION):
    # define jsonld for this item
    return {
        "@context": at_context,
        "@type": "reproschema:Field",
        "@id": item_name,
        "prefLabel": item_name,
        "schema:description": item_name,
        "schema:schemaVersion": VERSION,
        "schema:version": VERSION,
        "ui": {"allow": ["skipped"], "inputType": []},
        "question": {"en": question},
    }


def define_response_choice(response_type, response_choices):
    # now we define the answers for this item
    if response_type == "boolean":

        inputType = "radio"

        responseOptions = {
            "multipleChoice": False,
            "choices": [
                {"schema:value": 0, "schema:name": "No", "@type": "schema:option"},
                {"schema:value": 1, "schema:name": "Yes", "@type": "schema:option"},
                {"schema:value": 9, "schema:name": "Unknown", "@type": "schema:option"},
            ],
        }

    # if we have multiple choices with a radio item
    elif response_type == "radio":

        inputType = "radio"

        responseOptions = {"choices": []}

        responseOptions = list_responses_options(responseOptions, response_choices)

    # if we have a dropdown menu
    elif response_type == "dropdown":

        inputType = "select"

        responseOptions = {"choices": []}

        responseOptions = list_responses_options(responseOptions, response_choices)

    # response is date
    elif response_type == "date":
        inputType = "date"
        responseOptions = {"valueType": "xsd:date"}

    # response is time range
    elif response_type == "time range":
        inputType = "timeRange"
        responseOptions = {"valueType": "datetime"}

    # response is slider

    elif response_type == "slider":
        inputType = "slider"
        responseOptions = {
            "valueType": "xsd:integer",
            "schema:minValue": 0,
            "schema:maxValue": 6,
            "choices": [
                {
                    "schema:name": "Not at all",
                    "schema:value": 0,
                    "@type": "schema:option",
                },
                {"schema:value": 1, "@type": "schema:option"},
                {"schema:value": 2, "@type": "schema:option"},
                {"schema:value": 3, "@type": "schema:option"},
                {"schema:value": 4, "@type": "schema:option"},
                {"schema:value": 5, "@type": "schema:option"},
                {
                    "schema:name": "Completely",
                    "schema:value": 6,
                    "@type": "schema:option",
                },
            ],
        }

    # response is integer
    elif response_type == "int":
        inputType = "number"
        responseOptions = {"valueType": "xsd:integer"}

    # response is float
    elif response_type == "float":
        inputType = "float"
        responseOptions = {"valueType": "xsd:float"}

    # input requires typed answer
    elif response_type == "char":
        inputType = "text"
        responseOptions = {"type": "xsd:string"}

    else:
        inputType = "text"
        responseOptions = {"type": "xsd:string"}

    return inputType, responseOptions


def list_responses_options(responseOptions, response_choices):

    for i, opt in enumerate(response_choices):

        responseOptions["choices"].append(
            {"schema:name": opt, "schema:value": i, "@type": "schema:option"}
        )

    responseOptions["choices"].append(
        {
            "schema:name": "Other",
            "schema:value": len(response_choices) + 1,
            "@type": "schema:option",
        }
    )

    return responseOptions
