def get_item_info(row, CSV_INFO):

    item_name = []

    item_col = CSV_INFO["item"]["col"]
    item_col_name = CSV_INFO["item"]["name"]

    # we want to skip the header and only include items with 1 in the include column (if it exists)
    INCLUDE = True
    incl_col = CSV_INFO["include"]["col"]
    if row[item_col] == item_col_name or (incl_col != [] and row[incl_col] != "1"):

        print("   skipping item")

        return {"name": item_name}

    item_name = row[item_col].replace("\n", "")

    question_col = CSV_INFO["question"]["col"]
    question = row[question_col].replace("\n", "")

    resp_type_col = CSV_INFO["resp_type"]["col"]
    response_type = row[resp_type_col]

    choice_col = CSV_INFO["choice"]["col"]
    response_choices = row[choice_col].split(" | ")

    visibility = get_visibility(row, CSV_INFO)

    mandatory = get_mandatory(row, CSV_INFO)

    return {
        "name": item_name,
        "question": question,
        "resp_type": response_type,
        "choices": response_choices,
        "visibility": visibility,
    }


def get_visibility(row, CSV_INFO):

    visibility = True

    if row[CSV_INFO["vis"]["col"]] != "1":

        visibility = row[CSV_INFO["vis"]["col"]]

        # vis_conditions = row[choice_col].split(',')
        #
        # for i, cdt in enumerate(vis_conditions):
        #
        #     visibility['choices'].append({
        #         'schema:name': opt,
        #         'schema:value': i,
        #         '@type': 'schema:option'
        #         })

    return visibility


def get_mandatory(row, CSV_INFO):

    mandatory = False

    if row[CSV_INFO["mandatory"]["col"]] == "1":

        mandatory = True

    return mandatory


def define_new_item(item_info, REPRONIM_REPO, VERSION):
    # define jsonld for this item

    item_schema = {
        "@context": REPRONIM_REPO + "contexts/generic",
        "@type": "reproschema:Field",
        "@id": item_info["name"],
        "prefLabel": item_info["name"],
        "schema:description": item_info["name"],
        "schema:schemaVersion": VERSION,
        "schema:version": VERSION,
        "ui": {"allow": ["reproschema:Skipped"], "inputType": []},
        "question": {"en": item_info["question"]},
    }

    inputType, responseOptions = define_response_choice(
        item_info["resp_type"], item_info["choices"]
    )

    item_schema["ui"]["inputType"] = inputType
    item_schema["responseOptions"] = responseOptions

    return item_schema


def define_response_choice(response_type, response_choices):
    # now we define the answers for this item

    # default (also valid for "char" input type)
    inputType = "text"
    responseOptions = {"type": "xsd:string"}

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
        responseOptions = slider_response(response_choices, "min", "max")

    # response is integer
    elif response_type == "int":
        inputType = "number"
        responseOptions = {"valueType": "xsd:integer"}

    # response is float
    elif response_type == "float":
        inputType = "float"
        responseOptions = {"valueType": "xsd:float"}

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


def slider_response(response_choices, min_label, max_label):

    from numpy import linspace

    min = int(response_choices[0])
    max = int(response_choices[1])
    steps = int(response_choices[2]) + 1 if len(response_choices) == 3 else 101
    responseOptions = {
        "valueType": "xsd:integer",
        "schema:minValue": min,
        "schema:maxValue": max,
        "choices": [],
    }

    for i in linspace(min, max, steps):
        responseOptions["choices"].append({"schema:value": i, "@type": "schema:option"})

    responseOptions["choices"][0]["schema:name"] = min_label
    responseOptions["choices"][-1]["schema:name"] = max_label

    return responseOptions
