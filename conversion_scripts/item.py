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

