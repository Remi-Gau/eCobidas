from reproschema_schema import ReproschemaSchema


class ReproschemaItem(ReproschemaSchema):
    """
    class to deal with reproschema activities
    """

    def __init__(self, VERSION="1.0.0-rc1"):
        super().__init__(VERSION)
        self.schema["@type"] = "reproschema:Field"
        self.schema["ui"] = {"inputType": []}
        self.schema["question"] = {}
        self.schema["responseOptions"] = {}

    def set_URI(self, URI):
        self.URI = URI

    def set_defaults(self, name):
        self._ReproschemaSchema__set_defaults(name)  # this looks wrong
        self.schema_file = name
        self.schema["@id"] = name

    def set_question(self, question, lang="en"):
        self.schema["question"][lang] = question

    def set_input_type(self, input_type):
        self.schema["ui"]["inputType"] = input_type

    def set_response_options(self, response_options):
        self.schema["responseOptions"] = response_options

    def sort(self):
        """
        sort the dictionnary so the different keys are printed in a typical
        order
        """
        schema_order = [
            "@context",
            "@type",
            "@id",
            "prefLabel",
            "description",
            "schemaVersion",
            "version",
            "ui",
            "question",
            "responseOptions",
        ]

        reordered_dict = {k: self.schema[k] for k in schema_order}
        self.schema = reordered_dict

        # ui_order = [
        #     "order",
        #     "shuffle",
        #     "addProperties",
        # ]

        # reordered_dict = {k: self.schema["ui"][k] for k in ui_order}
        # self.schema["ui"] = reordered_dict
