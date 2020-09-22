from reproschema_schema import ReproschemaSchema


class ReproschemaProtocol(ReproschemaSchema):
    """
    class to deal with reproschema protocols
    """

    def __init__(self, VERSION):
        super().__init__(VERSION)
        self.schema["@type"] = "reproschema:Protocol"
        self.schema["ui"] = (
            {"allow": [], "shuffle": [], "order": [], "addProperties": []},
        )

    def set_landing_page(self, landing_page_url, lang="en"):
        self.schema["landingPage"] = {"@id": landing_page_url, "@language": lang}

    # TODO
    # def add_landing_page(self, landing_page_url, lang="en"):

    def set_image(self, image_url):
        self.schema["image"] = image_url

    def set_ui_allow(self):
        self.schema["ui"]["allow"] = [
            "reproschema:AutoAdvance",
            "reproschema:AllowExport",
        ]

    def set_ui_shuffle(self, shuffle=False):
        self.schema["ui"]["shuffle"] = shuffle

    def set_defaults(self, name):
        super().__set_defaults(name)
        self.set_landing_page("../../README-en.md")
        self.set_ui_allow()
        self.set_ui_shuffle(False)

    def append_activity(self, activity):

        # update the content of the protool schema and context wrt this new activity
        append_to_protocol = {
            "variableName": activity.get_name,
            "isAbout": activity.URI,
            # for the name displayed by the UI for this activity we simply reuse the
            # activity name
            "prefLabel": {"en": activity.prefLabel},
            "isVis": True,
        }

        self.schema["ui"]["order"].append(activity.URI)
        self.schema["ui"]["addProperties"].append(append_to_protocol)
