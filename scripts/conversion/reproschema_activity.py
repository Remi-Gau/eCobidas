from reproschema_schema import ReproschemaSchema


class ReproschemaActivity(ReproschemaSchema):
    """
    class to deal with reproschema activities
    """

    def __init__(self):
        super().__init__()
        self.schema["@type"] = "reproschema:Activity"
        self.schema["ui"] = {"shuffle": [], "order": [], "addProperties": []}

    def set_ui_shuffle(self, shuffle=False):
        self.schema["ui"]["shuffle"] = shuffle

    def set_URI(self, URI):
        self.URI = URI

    def get_URI(self):
        return self.URI

    # TODO
    # preamble
    # compute
    # citation
    # image

    def set_defaults(self, name):
        self._ReproschemaSchema__set_defaults(name)  # this looks wrong
        self.set_ui_shuffle(False)

    def update_activity(self, item_info):

        # TODO
        # - remove the hard coding on visibility and valueRequired

        # update the content of the activity schema with new item

        item_info["URI"] = "items/" + item_info["name"]

        append_to_activity = {
            "variableName": item_info["name"],
            "isAbout": item_info["URI"],
            "isVis": item_info["visibility"],
            "valueRequired": False,
        }

        self.schema["ui"]["order"].append(item_info["URI"])
        self.schema["ui"]["addProperties"].append(append_to_activity)

    def sort(self):
        schema_order = [
            "@context",
            "@type",
            "@id",
            "prefLabel",
            "description",
            "schemaVersion",
            "version",
            "ui",
        ]
        self.sort_schema(schema_order)

        ui_order = [
            "shuffle",
            "order",
            "addProperties",
        ]
        self.sort_ui(ui_order)
