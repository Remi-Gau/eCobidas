import os
import sys
import csv

from item import get_item_info, define_new_item

from utils import (
    get_metatable,
    load_data,
    print_item_to_table,
)

sep = ", "

pattern = "artemis-"

header = ["item", "field", "question", "options", "instructions"]

with open("names.csv", "w", newline="") as csvfile:

    writer = csv.DictWriter(csvfile, fieldnames=header)

    writer.writerow(
        {
            "item": "ARTEM-IS (Agreed Reporting Template for EEG Methodology - International Standard) template for ERP"
        }
    )
    writer.writeheader()

    df = get_metatable()

    tables_to_convert = df[df["schema"].str.match(r"(^" + pattern + ".*)") == True]
    tables_name = list(tables_to_convert["basename"])
    tables_to_convert = list(tables_to_convert["schema"])

    for j, this_table in enumerate(tables_to_convert):

        df = load_data(this_table)

        activities = list(df.activity_order.unique())

        for i, activity_idx in enumerate(activities):

            print(str(activity_idx) + " - " + tables_name[j].upper())
            writer.writerow(
                {"item": str(activity_idx) + " - " + tables_name[j].upper()}
            )

            this_activity = df["activity_order"] == activities[i]

            items = df[this_activity]
            included_items = items["include"] == 1
            items = items[included_items]

            items_order = items.item_order.unique()

            for item_idx in items_order:

                this_item = items[items["item_order"] == item_idx]
                item_info = get_item_info(this_item)

                dict_to_print = print_item_to_table(
                    activity_idx, item_idx, this_item, item_info, sep
                )

                writer.writerow(dict_to_print)
