import math
from pathlib import Path

import pandas as pd
from loguru import logger
from reproschema.models.activity import Activity
from reproschema.models.item import ResponseOption
from reproschema.models.protocol import Protocol

from ecobidas.item import define_new_item, get_item_info
from ecobidas.utils import (
    get_landing_page,
    get_output_dir,
    get_schema_info,
    load_data,
    print_info,
    print_item_info,
    root_dir,
    snake_case,
)


def create_schema(
    this_schema: str, output_dir: None | str | Path = None, debug: bool = False
) -> Protocol:
    """
    Take the content of the a csv file and turns it into a reproschema protocol.

    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encounters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """
    if output_dir is None:
        output_dir = root_dir()
    # add a way to deal with this_schelma being a file
    df = load_data(this_schema)

    logger.debug(f"{this_schema=}; {output_dir=}")

    output_dir = get_output_dir(this_schema, output_dir)

    schema_info = get_schema_info(this_schema)

    if schema_info["dir"] == "response_options":
        create_response_options(schema_info, df, output_dir)
        return

    protocol, protocol_path = initialize_protocol(this_schema, output_dir)

    # TODO implement once figured out wha the right schema shape is
    # protocol.schema["citation"] = ""
    # if schema_info["citation"].any():
    #     protocol.schema["citation"] = schema_info["citation"].tolist()[0]

    activities = list(df.activity_order.unique())

    if debug:
        activities = [1]

    for activity_idx in activities:
        this_activity = df["activity_order"] == activity_idx
        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        activity, activity_path = initialize_activity(items, output_dir)

        # TODO implement once figured out what the right schema shape is
        # activity.schema["citation"] = ""
        # if schema_info["citation"].any():
        #     activity.schema["citation"] = schema_info["citation"].tolist()[0]

        preamble = make_preamble(schema_info, items)
        activity.set_preamble(preamble)

        items_order = items.item_order.unique()

        # TODO add a check to make sure that no 2 items have the same
        # ID (OR preferred label)

        for item_idx in items_order:
            this_item = items[items["item_order"] == item_idx]

            item_info = get_item_info(this_item)

            if item_info.get("message"):
                activity.messages.append(item_info["message"])

            print_item_info(str(activity_idx), item_idx, item_info)

            item = define_new_item(item_info)

            item.write(Path(activity_path) / "items")

            activity.append_item(item)

        activity.URI = str(activity_path).replace(str(output_dir), "..") + "/" + activity.at_id
        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.write(protocol_path)

    logger.info(f"\nProtocol saved at: {protocol_path}")

    return protocol


def initialize_protocol(this_schema: Path | str, output_dir: Path) -> tuple[Protocol, Path]:
    schema_info = get_schema_info(this_schema)

    protocol_name = snake_case(schema_info["basename"])

    # TODO
    # are we sure we want to change the case or the protocol
    # or make it snake case?
    protocol_name = protocol_name.lower()
    protocol_path = output_dir / "protocols"

    protocol = Protocol(name=protocol_name, output_dir=protocol_path, preamble={"en": ""})
    protocol.set_landing_page(get_landing_page(schema_info))
    protocol.ui.shuffle = False
    protocol.write(protocol_path)

    print_info("protocol", protocol_name, protocol.URI)

    return protocol, protocol_path


def initialize_activity(items: pd.DataFrame, output_dir: str | Path) -> tuple[Activity, Path]:
    if len(items.activity_pref_label.unique()) == 0:
        raise NameError("Empty activity")

    activity_pref_label = items.activity_pref_label.unique()[0]
    activity_name = snake_case(activity_pref_label)
    activity_name = activity_name.lower()

    activity = Activity(
        name=activity_name,
        prefLabel=activity_pref_label,
        output_dir=f"{output_dir}/activities/{activity_name}/",
        messages=[],
    )

    print_info("activity", activity_pref_label, activity.URI)

    return activity, Path(activity.URI).parent


def get_activity_preamble(items: pd.DataFrame) -> str:
    if "preamble" not in items:
        return ""

    not_nan = items["preamble"].notna()

    preambles = items[not_nan]
    preamble = list(preambles["preamble"].unique())

    preamble = "" if len(preamble) > 1 or not preamble else preamble[0]
    return preamble


def create_response_options(
    schema_info: dict[str, str], df: pd.DataFrame, output_dir: str | Path
) -> None:
    responses = df.name.unique()

    response_options = ResponseOption(valueType="xsd:integer")
    response_options.set_defaults()
    response_options.multipleChoice = False

    for i, name in enumerate(responses):
        if isinstance(name, float) and math.isnan(name):
            name = "None"
        response_options.add_choice(name, i)
        response_options.set_max(i)

    response_options.write(output_dir)

    print_info(
        "response options",
        schema_info["basename"],
        str(Path(output_dir) / response_options.at_id),
    )


def make_preamble(schema_info: dict[str, str], items: pd.DataFrame) -> str:
    """Do nothing if preamble is empty.

    but otherwise we try to create an additional 'header' to the activity
    with info about the source spreadsheet, repo...
    """
    preamble = get_activity_preamble(items)

    if not preamble:
        return preamble

    info = {
        "preamble": preamble,
        "xls": schema_info["link"],
        "repo": "",
        "citation": "",
    }

    if schema_info["repo"]:
        info["repo"] = schema_info["repo"]
    if schema_info["citation"]:
        info["citation"] = schema_info["citation"]

    preamble = (
        "<p>"
        + "<a href='"
        + str(info["xls"])
        + "' target='_blank' > Source </a> | "
        + "<a href='"
        + str(info["repo"])
        + "' target='_blank' > GitHub repository </a> | "
        + "<a href='"
        + str(info["citation"])
        + "' target='_blank' > Reference </a>"
        + "<br><br>"
        + str(preamble)
        + "</p>"
    )

    return preamble
