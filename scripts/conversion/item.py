def get_item_info(row, csv_info):

    item_name = []

    item_col = csv_info["item"]["col"]
    item_col_name = csv_info["item"]["name"]

    # we want to skip the header and only include items with 1 in the include column (if it exists)
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
    """
    define jsonld for this item
    """

    from reproschema_item import ReproschemaItem

    item = ReproschemaItem()

    item.set_defaults(item_info["name"])

    item.set_question(item_info["question"])

    item = define_response_choices(item, item_info["resp_type"], item_info["choices"])

    return item


def define_response_choices(item, response_type, response_choices):

    # in case we have one of the basic response type
    # with no response choice involved
    item.set_basic_response_type(response_type)

    if response_type == "radio":
        response_options = list_responses_options(response_choices)
        item.set_input_type_as_radio(response_options)

    # if we have a dropdown menu
    # TODO: change to select item to have a REAL dropdown as soon as radio item
    # offer the possibility to have an "Other" choice that opens a text box
    elif response_type == "dropdown":
        response_options = list_responses_options(response_choices)
        item.set_input_type_as_radio(response_options)

    elif response_type == "slider":
        # response_options = slider_response(response_choices, min_label, max_label)
        # item.set_input_type_as_slider(response_options)
        item.set_input_type_as_slider()

    if (
        response_type == "boolean"
        or response_type == "mri_software"
        or response_type == "interpolation"
        or response_type == "cost_function"
        or response_type == "multiple_comparison"
    ):

        value_constraint = response_type

        if "_" in response_type:
            """
            if response_type is "test_name" in the spreadsheet then the
            corresponding response option value constraints file is
            testNameValueConstraints, so we need to do some string magic
            """

            response_type = response_type.split("_")

            # This does not cover the cases where the string has more than
            # 2 elements separated by "_"
            value_constraint = (
                response_type[0] + response_type[1][0].upper() + response_type[1][1:]
            )

        response_options = "../../../response_options/"
        response_options += value_constraint
        response_options += "ValueConstraints"

        item.set_input_type_as_radio(response_options)

    return item


def list_responses_options(response_choices):

    response_options = {"choices": []}

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
