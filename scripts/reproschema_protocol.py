from reproschema_schema import ReproschemaSchema


class ReproschemaProtocol(ReproschemaSchema):
    """
    class to deal with reproschema protocols
    """

    def __init__(self):
        super().__init__()
        self.schema["@type"] = "reproschema:Protocol"
        self.schema["ui"] = {
            "allow": [],
            "shuffle": [],
            "order": [],
            "addProperties": [],
        }

    def set_landing_page(self, landing_page_url, lang="en"):
        self.schema["landingPage"] = {"@id": landing_page_url, "@language": lang}

    # TODO
    # def add_landing_page(self, landing_page_url, lang="en"):
    # preamble
    # compute

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
        self._ReproschemaSchema__set_defaults(name)  # this looks wrong
        self.set_landing_page("../../README-en.md")
        self.set_ui_allow()
        self.set_ui_shuffle(False)

    def append_activity(self, activity):

        # TODO
        # - remove the hard coding on visibility and valueRequired

        # update the content of the protocol with this new activity
        append_to_protocol = {
            "variableName": activity.get_name(),
            "isAbout": activity.get_URI(),
            "prefLabel": {"en": activity.schema["prefLabel"]},
            "isVis": True,
            "valueRequired": False,
        }

        self.schema["ui"]["order"].append(activity.URI)
        self.schema["ui"]["addProperties"].append(append_to_protocol)

    def sort(self):
        schema_order = [
            "@context",
            "@type",
            "@id",
            "prefLabel",
            "description",
            "schemaVersion",
            "version",
            "landingPage",
            "ui",
        ]
        self.sort_schema(schema_order)

        ui_order = [
            "allow",
            "shuffle",
            "order",
            "addProperties",
        ]
        self.sort_ui(ui_order)

