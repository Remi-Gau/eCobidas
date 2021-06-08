from numpy import linspace

from utils import convert_to_str, convert_to_int, snake_case
from reproschema.models.item import Item, ResponseOption


def get_item_info(this_item):

    item_name = []

    pref_label = convert_to_str(this_item["item_pref_label"])
    description = convert_to_str(this_item["item_description"])

    item_name = snake_case(pref_label)

    question = convert_to_str(this_item["question"])
    question = question.replace("\n", "")

    field_type = convert_to_str(this_item["field_type"])
    if field_type == "integer":
        field_type = "int"

    choices = convert_to_str(this_item["choices"])
    if type(choices) == str:
        choices = choices.split(" | ")

    visibility = get_visibility(this_item)

    mandatory = get_mandatory(this_item)

    return {
        "name": item_name,
        "pref_label": pref_label,
        "description": description,
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

    item = Item()
    item.set_defaults(item_info["name"])
    item.set_description(item_info["description"])
    item.set_pref_label(item_info["pref_label"])
    item.set_question(item_info["question"])
    item = define_choices(item, item_info["field_type"], item_info["choices"])

    return item


def define_choices(item, field_type, choices):

    # in case we have one of the basic response type
    # with no response choice involved
    item.set_basic_response_type(field_type)

    if field_type == "multitext":
        item.set_input_type_as_multitext()

    elif field_type == "radio":
        response_options = list_responses_options(choices)
        item.set_input_type_as_radio(response_options)

    # if we have a dropdown menu
    # TODO: change to select item to have a REAL dropdown as soon as radio item
    # offer the possibility to have an "Other" choice that opens a text box
    elif field_type == "dropdown":
        response_options = list_responses_options(choices)
        item.set_input_type_as_select(response_options)

    elif field_type == "slider":
        response_options = slider_response(choices)
        item.set_input_type_as_slider(response_options)

    if field_type in ["radio", "dropdown"] and ispreset(choices):
        item = use_preset(item, choices)

    return item


def list_responses_options(choices):

    response_options = ResponseOption()

    for i, opt in enumerate(choices):

        response_options.add_choice(opt, i)

    response_options.add_choice("Other", len(choices))

    response_options.set_min(0)
    response_options.set_max(len(choices))

    return response_options


def slider_response(choices):

    min = int(choices[0])
    max = int(choices[1])
    steps = int(choices[2]) if len(choices) == 3 else 11

    response_options = ResponseOption()
    response_options.set_max(min)
    response_options.set_max(max)

    for i, opt in enumerate(linspace(min, max, steps)):
        response_options.add_choice(str(opt), i)

    return response_options


def use_preset(item, choices):

    preset_response_file = (
        "https://raw.githubusercontent.com/ohbm/eCOBIDAS/master/response_options/"
        + choices[0].split("preset:")[1]
        + ".jsonld"
    )

    item.response_options.options = preset_response_file

    return item


def ispreset(choices):
    return isinstance(choices[0], str) and len(choices) == 1 and "preset:" in choices[0]
