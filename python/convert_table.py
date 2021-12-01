import csv
from rich import print

from item import get_item_info

from utils import (
    get_metatable,
    load_data,
    print_item_to_table,
)


def main():

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

                id = str(activity_idx) + " - " + tables_name[j].upper()

                print("[bold red]" + id + "[/bold red]")
                writer.writerow({"item": id})

                this_activity = df["activity_order"] == activities[i]

                items = df[this_activity]
                included_items = items["include"] == 1
                items = items[included_items]

                items_order = items.item_order.unique()

                sub_section = ""
                sub_section_id = 0

                for item_idx in items_order:

                    this_item = items[items["item_order"] == item_idx]
                    item_info = get_item_info(this_item)

                    if item_info["sub_section"] not in ["", sub_section]:
                        sub_section_id += 1
                        item_id = 0
                        sub_section = item_info["sub_section"]
                        id = (
                            str(activity_idx)
                            + "."
                            + str(sub_section_id)
                            + " - "
                            + sub_section.upper()
                        )
                        writer.writerow({"item": id})

                    item_id += 1
                    id = (
                        str(activity_idx)
                        + "."
                        + str(sub_section_id)
                        + "."
                        + str(item_id)
                    )

                    dict_to_print = print_item_to_table(id, this_item, item_info, sep)

                    writer.writerow(dict_to_print)


if __name__ == "__main__":

    main()