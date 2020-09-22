from reproschema_schema import ReproschemaSchema


class ReproschemaActivity(ReproschemaSchema):
    """
    class to deal with reproschema activities
    """

    def __init__(self, VERSION="1.0.0-rc1"):
        super().__init__(VERSION)
        self.schema["@type"] = "reproschema:Activity"
        self.schema["ui"] = {"shuffle": [], "order": [], "addProperties": []}

    def set_ui_shuffle(self, shuffle=False):
        self.schema["ui"]["shuffle"] = shuffle

    def set_URI(self, URI):
        self.URI = URI

    def set_defaults(self, name):
        self._ReproschemaSchema__set_defaults(name)  # this looks wrong
        self.set_ui_shuffle(False)

    def update_activity(self, item_info):
        # update the content of the activity schema with new item

        item_info["URI"] = "items/" + item_info["name"]

        append_to_activity = {
            "variableName": item_info["name"],
            "isAbout": item_info["URI"],
            "isVis": item_info["visibility"],
        }

        self.schema["ui"]["order"].append(item_info["URI"])
        self.schema["ui"]["addProperties"].append(append_to_activity)

