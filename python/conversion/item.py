from utils import convert_to_str, convert_to_int, snake_case
from reproschema_item import ReproschemaItem


def get_item_info(this_item):

    item_name = []

    pref_label = convert_to_str(this_item["item_pref_label"])

    item_name = snake_case(pref_label)

    question = convert_to_str(this_item["question"])
    question = question.replace("\n", "")

    field_type = convert_to_str(this_item["field_type"])

    choices = convert_to_str(this_item["choices"])
    if type(choices) == str:
        choices = choices.split(" | ")

    visibility = get_visibility(this_item)

    mandatory = get_mandatory(this_item)

    return {
        "name": item_name,
        "pref_label": pref_label,
        "question": question,
        "field_type": field_type,
        "choices": choices,
        "visibility": visibility,
        "mandatory": mandatory,
    }


def get_visibility(this_item):

    visibility = convert_to_str(this_item["visibility"])

    if visibility in ["1", 1]:
        visibility = True

    elif visibility in ["0", 0]:
        visibility = False

    # TODO
    # help with javascript expression input and validation

    return visibility


def get_mandatory(this_item):

    mandatory = convert_to_int(this_item["mandatory"])

    mandatory = mandatory >= 0

    return mandatory


def define_new_item(item_info):
    """
    define jsonld for this item
    """

    item = ReproschemaItem()

    item.set_defaults(item_info["name"])
    item.set_pref_label(item_info["pref_label"])

    item.set_question(item_info["question"])

    item = define_choices(item, item_info["field_type"], item_info["choices"])

    return item


def define_choices(item, field_type, choices):

    # in case we have one of the basic response type
    # with no response choice involved
    item.set_basic_response_type(field_type)

    if field_type == "radio":
        choices = list_responses_options(choices)
        choices["multipleChoice"] = False
        item.set_input_type_as_radio(choices)

    # if we have a dropdown menu
    # TODO: change to select item to have a REAL dropdown as soon as radio item
    # offer the possibility to have an "Other" choice that opens a text box
    elif field_type == "dropdown":
        choices = list_responses_options(choices)
        choices["multipleChoice"] = False
        item.set_input_type_as_select(choices)

    elif field_type == "slider":
        # choices = slider_response(choices, min_label, max_label)
        # item.set_input_type_as_slider(choices)
        item.set_input_type_as_slider()

    if field_type in [
        "boolean",
        "mri_software",
        "interpolation",
        "cost_function",
        "multiple_comparison",
    ]:

        value_constraint = field_type

        if "_" in field_type:
            """
            if field_type is "test_name" in the spreadsheet then the
            corresponding response option value constraints file is
            testNameValueConstraints, so we need to do some string magic
            """

            field_type = field_type.split("_")

            # This does not cover the cases where the string has more than
            # 2 elements separated by "_"
            value_constraint = (
                field_type[0] + field_type[1][0].upper() + field_type[1][1:]
            )

        # TODO
        # do not hard code the path of where the response options files are stored
        choices = "../../../choices/"
        choices += value_constraint
        choices += "ValueConstraints"

        item.set_input_type_as_radio(choices)

    return item


def list_responses_options(choice_list):

    choices = {"choices": []}

    for i, opt in enumerate(choice_list):

        choices["choices"].append({"name": opt, "value": i})

    choices["choices"].append({"name": "Other", "value": len(choice_list)})

    choices["minValue"] = 0
    choices["maxValue"] = len(choices["choices"]) - 1
    choices["valueType"] = "xsd:integer"

    return choices


def slider_response(choices, min_label, max_label):

    from numpy import linspace

    # min = int(choices[0])
    # max = int(choices[1])
    # steps = int(choices[2]) + 1 if len(choices) == 3 else 11
    min = 1
    max = 11
    steps = 11
    choices = {
        "valueType": "xsd:integer",
        "minValue": min,
        "maxValue": max,
        "choices": [],
    }

    for i in linspace(min, max, steps):
        choices["choices"].append({"value": int(i), "@type": "option"})

    choices["choices"][0]["name"] = min_label
    choices["choices"][-1]["name"] = max_label

    return choices
