import re

from loguru import logger
from numpy import isnan, linspace
from reproschema.models.item import Item, ResponseOption

from .utils import convert_to_int, convert_to_str, snake_case


def set_item_name(this_item: dict) -> str:
    if (
        "item" not in this_item
        or isinstance(convert_to_str(this_item["item"]), float)
        or convert_to_str(this_item["item"]) == ""
    ):
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

    unit: str | list[str] = ""
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

    choices: str | list[str] = convert_to_str(this_item["choices"])
    choices = split_choices(choices)

    visibility = get_visibility(this_item)

    mandatory = get_mandatory(this_item)

    message = None
    if "validation" in this_item and this_item["validation"].any():
        tokens = convert_to_str(this_item["validation"]).split(",")
        if len(tokens) > 1:
            message = {"message": tokens[1].strip(), "jsExpression": tokens[0].strip()}

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
        "message": message,
    }


def split_choices(choices: str) -> str | list[str]:
    if isinstance(choices, str):
        choices = choices.split(" | ")
    return choices


def get_visibility(this_item: dict) -> str | float | bool:
    visibility: str | float
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


def define_unit(item: Item, units: str) -> Item:
    if not units:
        return item

    unit_options = [
        {
            "prefLabel": {"en": unit},
            "value": unit,
        }
        for unit in units
    ]
    item.response_options.unitOptions = unit_options

    return item


def define_new_item(item_info: dict) -> Item:
    """Define jsonld for this item."""
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

    item.set_question(item_info["question"])

    if "details" in item_info and item_info["details"] != "":
        item.schema["details"] = {"en": f"{item_info['details']}"}
        item.schema_order.append("details")

    item = define_choices(item, field_type=item_info["field_type"], choices=item_info["choices"])
    item = define_unit(item, item_info["unit"])

    return item


def define_choices(item: Item, field_type: str, choices: list) -> Item:
    # in case we have one of the basic response type
    # with no response choice involved
    item.set_input_type()

    if field_type in {"multitext", "text"}:
        return item

    if field_type in {"int", "float"}:
        if field_type == "int":
            field_type = "integer"

        response_options = ResponseOption()
        response_options.set_valueType(field_type)

        if choices and isinstance(choices, list):
            min_value = int(choices[0])
            response_options.set_min(min_value)
            if len(choices) > 1:
                max_value = int(choices[1])
                response_options.set_max(max_value)
        else:
            logger.warning(f"No min or max value defined for {field_type} item.")

        item.set_input_type(response_options)

        return item

    elif field_type == "slider":
        response_options = slider_response(choices)
        item.set_input_type(response_options)
        return item

    if field_type in {"radio", "radio_multiple", "select", "select_multiple"}:
        response_options = list_responses_options(choices)

        if field_type in {"radio_multiple", "select_multiple"}:
            response_options.multipleChoice = True

        item.set_input_type(response_options)

        if ispreset(choices):
            item = use_preset(item, choices)

    return item


def list_responses_options(choices: list) -> ResponseOption:
    response_options = ResponseOption()

    for i, opt in enumerate(choices):
        response_options.add_choice(opt, i)

    response_options.set_min(0)
    response_options.set_max(len(choices) - 1)

    return response_options


def slider_response(choices: list) -> ResponseOption:
    min = float(choices[0])
    max = float(choices[1])
    steps = int(choices[2]) if len(choices) == 3 else 21

    response_options = ResponseOption()
    response_options.set_max(1)
    response_options.set_max(steps - 1)

    # TODO update after render off slide item has been improved
    for i, opt in enumerate(linspace(min, max, steps)):
        response_options.add_choice(f"{opt:.3f}", i)

    return response_options


def use_preset(item: Item, choices: list) -> Item:
    preset_response_file = (
        "https://raw.githubusercontent.com/ohbm/cobidas_schema/master/response_options/"
        + choices[0].split("preset:")[1]
        + ".jsonld"
    )

    item.response_options.choices = preset_response_file

    return item


def ispreset(choices: list) -> bool:
    return isinstance(choices[0], str) and len(choices) == 1 and "preset:" in choices[0]
