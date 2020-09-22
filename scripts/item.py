def get_item_info(row, csv_info):

    item_name = []

    item_col = csv_info["item"]["col"]
    item_col_name = csv_info["item"]["name"]

    # we want to skip the header and only include items with 1 in the include column (if it exists)
    INCLUDE = True
    incl_col = csv_info["include"]["col"]
    if row[item_col] == item_col_name or (incl_col != [] and row[incl_col] != "1"):

        print("   skipping item")

        return {"name": item_name}

    item_name = row[item_col].replace("\n", "")

    question_col = csv_info["question"]["col"]
    question = row[question_col].replace("\n", "")

    resp_type_col = csv_info["resp_type"]["col"]
    response_type = row[resp_type_col]

    choice_col = csv_info["choice"]["col"]
    response_choices = row[choice_col].split(" | ")

    preamble = csv_info["preamble"]["col"]

    visibility = get_visibility(row, csv_info)

    mandatory = get_mandatory(row, csv_info)

    return {
        "name": item_name,
        "question": question,
        "resp_type": response_type,
        "choices": response_choices,
        "visibility": visibility,
        "preamble": preamble,
        "mandatory": mandatory,
    }


def get_visibility(row, csv_info):

    visibility = True

    if row[csv_info["vis"]["col"]] != "1":

        visibility = row[csv_info["vis"]["col"]]

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


def get_mandatory(row, csv_info):

    mandatory = False

    if row[csv_info["mandatory"]["col"]] == "1":

        mandatory = True

    return mandatory


def define_new_item(item_info):

    from reproschema_item import ReproschemaItem

    # define jsonld for this item

    item = ReproschemaItem()

    item.set_defaults(item_info["name"])

    item.set_question(item_info["question"])

    input_type, response_options = define_response_choice(
        item_info["resp_type"], item_info["choices"]
    )
    item.set_input_type(input_type)
    item.set_response_options(response_options)

    return item


def define_response_choice(response_type, response_choices):
    # now we define the answers for this item

    # default (also valid for "char" input type)
    input_type = "text"
    response_options = {"type": "xsd:string"}

    if response_type == "boolean":

        input_type = "radio"
        response_options = "../../../response_options/booleanValueConstraints"

    if response_type == "mri_software":

        input_type = "radio"
        response_options = "../../../response_options/mriSoftwareValueConstraints"

    if response_type == "interpolation":

        input_type = "radio"
        response_options = "../../../response_options/interpolationValueConstraints"

    if response_type == "cost_function":

        input_type = "radio"
        response_options = "../../../response_options/costFunctionValueConstraints"

    if response_type == "multiple_comparison":

        input_type = "select"
        response_options = (
            "../../../response_options/multipleComparisonValueConstraints"
        )

    # if we have multiple choices with a radio item
    elif response_type == "radio":

        input_type = "radio"
        response_options = {"choices": []}
        response_options = list_responses_options(response_options, response_choices)

    # if we have a dropdown menu
    elif response_type == "dropdown":

        input_type = "radio"  # "select"
        response_options = {"choices": []}
        response_options = list_responses_options(response_options, response_choices)

    # response is date
    elif response_type == "date":
        input_type = "date"
        response_options = {"valueType": "xsd:date"}

    # response is time range
    elif response_type == "time range":
        input_type = "timeRange"
        response_options = {"valueType": "datetime"}

    # response is slider
    elif response_type == "slider":
        input_type = "slider"
        # response_options = slider_response(response_choices, "min", "max")

    # response is integer
    elif response_type == "int":
        input_type = "number"
        response_options = {"valueType": "xsd:integer"}

    # response is float
    elif response_type == "float":
        input_type = "float"
        response_options = {"valueType": "xsd:float"}

    return input_type, response_options


def list_responses_options(response_options, response_choices):

    for i, opt in enumerate(response_choices):

        response_options["choices"].append({"name": opt, "value": i, "@type": "option"})

    response_options["choices"].append(
        {"name": "Other", "value": len(response_choices), "@type": "option"}
    )

    response_options["minValue"] = 0
    response_options["maxValue"] = len(response_choices)

    return response_options


def slider_response(response_choices, min_label, max_label):

    import numpy

    # min = int(response_choices[0])
    # max = int(response_choices[1])
    # steps = int(response_choices[2]) + 1 if len(response_choices) == 3 else 11
    min = 1
    max = 11
    steps = 11
    response_options = {
        "valueType": "xsd:integer",
        "minValue": min,
        "maxValue": max,
        "choices": [],
    }

    for i in numpy.linspace(min, max, steps):
        response_options["choices"].append({"value": int(i), "@type": "option"})

    response_options["choices"][0]["name"] = min_label
    response_options["choices"][-1]["name"] = max_label

    return response_options
