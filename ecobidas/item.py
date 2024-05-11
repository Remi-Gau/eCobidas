import re

from numpy import isnan, linspace
from reproschema.models.item import Item, ResponseOption

from .utils import convert_to_int, convert_to_str, snake_case


def set_item_name(this_item: dict):
    if "item" not in this_item.keys():
        item_name = convert_to_str(this_item["item_pref_label"])
    elif isinstance(convert_to_str(this_item["item"]), float):
        item_name = convert_to_str(this_item["item_pref_label"])
    elif convert_to_str(this_item["item"]) == "":
        item_name = convert_to_str(this_item["item_pref_label"])
    else:
        item_name = convert_to_str(this_item["item"])

    item_name = snake_case(item_name)
    item_name = re.sub("[^-_a-zA-Z0-9]+", "", item_name)

    return item_name


def get_item_info(this_item: dict) -> dict:
    sub_section = ""
    if "sub_section" in this_item and this_item["sub_section"].any():
        sub_section = convert_to_str(this_item["sub_section"])

    item_name = set_item_name(this_item)
    if "item_pref_label" in this_item:
        pref_label = convert_to_str(this_item["item_pref_label"])
    else:
        pref_label = item_name

    pref_label = pref_label.replace("_", " ")

    description = pref_label
    if "item_description" in this_item and this_item["item_description"].any():
        description = convert_to_str(this_item["item_description"])

    unit = ""
    if "unit" in this_item and this_item["unit"].any():
        unit = convert_to_str(this_item["unit"])
        unit = split_choices(unit)

    details = ""
    if "details" in this_item and this_item["details"].any():
        details = convert_to_str(this_item["details"])

    question = convert_to_str(this_item["question"])
    question = question.replace("\n", "")

    field_type = convert_to_str(this_item["field_type"])
    if field_type == "integer":
        field_type = "int"

    choices = convert_to_str(this_item["choices"])
    choices = split_choices(choices)

    visibility = get_visibility(this_item)

    mandatory = get_mandatory(this_item)

    return {
        "name": item_name,
        "pref_label": pref_label,
        "description": description,
        "question": question,
        "details": details,
        "field_type": field_type,
        "choices": choices,
        "unit": unit,
        "visibility": visibility,
        "mandatory": mandatory,
        "sub_section": sub_section,
    }


def split_choices(choices) -> list:
    if type(choices) == str:
        choices = choices.split(" | ")
    return choices


def get_visibility(this_item: dict):
    visibility = convert_to_str(this_item["visibility"])

    if visibility in ["1", 1]:
        visibility = True

    elif visibility in ["0", 0]:
        visibility = False

    elif isinstance(visibility, float) and isnan(visibility):
        visibility = True

    else:
        # TODO
        # help with javascript expression input and validation
        return visibility

    return visibility


def get_mandatory(this_item: dict) -> bool:
    mandatory = convert_to_int(this_item["mandatory"])

    mandatory = mandatory >= 0

    return mandatory


def define_unit(item, units):
    if units == "":
        return item

    unitOptions = [
        {
            "prefLabel": {"en": unit},
            "value": unit,
        }
        for unit in units
    ]
    item.response_options.options["unitOptions"] = unitOptions

    return item


def define_new_item(out_dir, item_info: dict):
    """
    define jsonld for this item
    """

    input_type = item_info["field_type"]
    if item_info["field_type"] == "int":
        input_type = "integer"
    if item_info["field_type"] == "radio_multiple":
        input_type = "radio"
    if item_info["field_type"] == "select_multiple":
        input_type = "select"

    item = Item(
        name=item_info["name"],
        description=item_info["description"],
        prefLabel=item_info["pref_label"],
        input_type=input_type,
        visible=item_info["visibility"],
        output_dir="items",
    )

    question = item_info["question"]
    if "id" in item_info and item_info["id"] != "":
        question = item_info["id"] + " - " + question
    if "details" in item_info and item_info["details"] != "":
        question = (
            question
            + "<div style='font-size: 70%; text-align:left;'><details> <summary> details </summary> <br>"
            + str(item_info["details"])
            + "</details></div>"
        )

    item.set_question(question)

    item = define_choices(item, field_type=item_info["field_type"], choices=item_info["choices"])
    item = define_unit(item, item_info["unit"])

    return item


def define_choices(item, field_type: str, choices: list):
    # in case we have one of the basic response type
    # with no response choice involved
    item.set_input_type()

    if field_type == "multitext":
        return item

    elif field_type == "slider":
        response_options = slider_response(choices)
        item.set_input_type(response_options)
        return item

    elif field_type == "text":
        return item

    if field_type in {"radio", "radio_multiple", "select", "select_multiple"}:
        response_options = list_responses_options(choices)

        if field_type in {"radio_multiple", "select_multiple"}:
            response_options.multipleChoice = True

        item.set_input_type(response_options)

        if ispreset(choices):
            item = use_preset(item, choices)

    return item


def list_responses_options(choices: list):
    response_options = ResponseOption()

    for i, opt in enumerate(choices):
        response_options.add_choice(opt, i)

    response_options.set_min(0)
    response_options.set_max(len(choices) - 1)

    return response_options


def slider_response(choices: list):
    min = float(choices[0])
    max = float(choices[1])
    steps = int(choices[2]) if len(choices) == 3 else 21

    response_options = ResponseOption()
    response_options.set_max(1)
    response_options.set_max(steps - 1)

    linspace(min, max, steps)

    # TODO update after render off slide item has been improved
    for i, opt in enumerate(linspace(min, max, steps)):
        response_options.add_choice(f"{opt:.3f}", i)

    return response_options


def use_preset(item, choices: list):
    preset_response_file = (
        "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/response_options/"
        + choices[0].split("preset:")[1]
        + ".jsonld"
    )

    item.response_options.choices = preset_response_file

    return item


def ispreset(choices: list):
    return isinstance(choices[0], str) and len(choices) == 1 and "preset:" in choices[0]
