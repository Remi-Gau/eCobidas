import os

from rich import print

from item import get_item_info, define_new_item
from utils import (
    snake_case,
    print_info,
    print_item_info,
    get_root_dir,
    get_landing_page,
    load_data,
    get_schema_info,
    get_output_dir,
)

from reproschema.models.activity import Activity
from reproschema.models.protocol import Protocol
from reproschema.models.item import ResponseOption

local_reproschema = os.path.join(
    get_root_dir(), "..", "reproschema-py", "reproschema", "models"
)
# sys.path.insert(0, local_reproschema)


def create_schema(this_schema, out_dir=get_root_dir(), debug=False):
    """
    This takes the content of the a csv file and turns it into a
    reproschema protocol.
    This loops through the items of the csv and creates a new reproschema
    activity with every new checklist "section" it encouters: this new activity
    will be added to the protocol.
    Every new item encountered is added to the current activity.
    """

    # add a way to deal with this_schelma being a file
    df = load_data(this_schema)
    out_dir = get_output_dir(this_schema, out_dir)

    schema_info = get_schema_info(this_schema)

    if schema_info["dir"].tolist()[0] == "response_options":
        create_response_options(schema_info, df, out_dir)
        return

    protocol, protocol_path = initialize_protocol(this_schema, out_dir)

    # TODO implement once figured out wha the right schema shape is
    # protocol.schema["citation"] = ""
    # if schema_info["citation"].any():
    #     protocol.schema["citation"] = schema_info["citation"].tolist()[0]

    activities = list(df.activity_order.unique())

    if debug:
        activities = [1]

    for i, activity_idx in enumerate(activities):
        this_activity = df["activity_order"] == activities[i]
        items = df[this_activity]
        included_items = items["include"] == 1
        items = items[included_items]

        protocol, activity, activity_path = initialize_activity(
            protocol, items, out_dir
        )

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

            item_info["id"] = f"{activity_idx:.0f}.{item_idx:.0f}"

            print_item_info(activity_idx, item_idx, item_info)

            item = create_new_item(item_info, activity_path)

            activity.append_item(item)

        activity.write(activity_path)

        protocol.append_activity(activity)

    protocol.write(protocol_path)

    return protocol


def initialize_protocol(this_schema, out_dir):
    schema_info = get_schema_info(this_schema)

    protocol_name = snake_case(schema_info["basename"].tolist()[0])
    # TODO
    # are we sure we want to change the case or the protocol
    # or make it snake case?
    protocol_name = protocol_name.lower()
    protocol = Protocol()
    protocol.set_defaults(protocol_name)

    protocol.set_landing_page(get_landing_page(schema_info))

    # create output directories
    protocol_path = os.path.join(out_dir, "protocols")
    protocol.set_directory = protocol_path
    if not os.path.exists(protocol_path):
        os.makedirs(protocol_path)

    protocol.write(protocol_path)

    print_info(
        "protocol", protocol_name, os.path.join(protocol_path, protocol.get_filename())
    )

    return protocol, protocol_path


def initialize_activity(protocol, items, out_dir):
    if len(items.activity_pref_label.unique()) == 0:
        raise NameError("Empty activity")

    activity = Activity()

    # TODO : make sure there is only only preferred label
    activity_pref_label = items.activity_pref_label.unique()[0]
    activity.set_pref_label(activity_pref_label)

    activity_name = snake_case(activity_pref_label)
    activity_name = activity_name.lower()
    # TODO
    # are we sure we want to change the case of the activity
    # or make it snake case?
    # try to get the name of the activity from the correct column in the TSV
    activity.set_defaults(activity_name)
    activity.set_filename(activity_name)
    activity.set_pref_label(activity_pref_label)

    URI = (
        "../activities"
        + "/"
        + activity.get_basename().replace("_schema", "")
        + "/"
        + activity.get_filename()
    )
    activity.set_URI(URI)

    activity_path = os.path.join(out_dir, "activities", activity.dir)

    if not os.path.exists(activity_path):
        os.makedirs(activity_path)

    if not os.path.exists(os.path.join(activity_path, "items")):
        os.makedirs(os.path.join(activity_path, "items"))

    print_info(
        "activity",
        activity_pref_label,
        os.path.join(activity_path, activity.get_filename()),
    )

    return protocol, activity, activity_path


def create_new_item(item_info: dict, activity_path: str):
    item = define_new_item(item_info)

    item.set_URI(os.path.join("items", item.get_filename()))

    # TODO
    # add a method to the Item class so that updating visibility does not have
    # does not have to be done manually
    item.visible = item_info["visibility"]

    item.write(os.path.join(activity_path, "items"))

    return item


def get_activity_preamble(items):
    if "preamble" not in items.keys():
        return ""

    not_nan = items["preamble"].notna()

    preambles = items[not_nan]
    preamble = list(preambles["preamble"].unique())

    preamble = "" if len(preamble) > 1 or not preamble else preamble[0]
    return preamble


def create_response_options(schema_info: dict, df, out_dir):
    responses = df.name.unique()

    response_options = ResponseOption()
    response_options.set_defaults()
    response_options.set_filename(schema_info["basename"].tolist()[0])
    response_options.set_type("integer")
    response_options.unset("multipleChoice")

    for i, name in enumerate(responses):
        response_options.add_choice(name, i)
        response_options.set_max(i)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    response_options.write(out_dir)

    print_info(
        "response options",
        schema_info["basename"].tolist()[0],
        os.path.join(out_dir, response_options.get_filename()),
    )


def make_preamble(schema_info, items):
    """
    if preamble is empty we do nothing
    but otherwise we try to create an additional 'header' to the activity
    with info about the source spreadsheet, repo...
    """

    preamble = get_activity_preamble(items)

    if not preamble:
        return preamble

    info = dict(
        preamble=preamble, xls=schema_info["link"].tolist()[0], repo="", citation=""
    )

    if schema_info["repo"].any():
        info["repo"] = schema_info["repo"].tolist()[0]
    if schema_info["citation"].any():
        info["citation"] = schema_info["citation"].tolist()[0]

    preamble = (
        "<p>"
        + "<a href='"
        + str(info["xls"])
        + "' target='_blank' > Source </a> | "
        + "<a href='"
        + str(info["repo"])
        + "' target='_blank' > Github repository </a> | "
        + "<a href='"
        + str(info["citation"])
        + "' target='_blank' > Reference </a>"
        + "<br><br>"
        + str(preamble)
        + "</p>"
    )

    return preamble
