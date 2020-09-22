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

    def set_question(self, question, lang="en"):
        self.schema["question"][lang] = question

    def set_input_type(self, input_type):
        self.schema["ui"]["inputType"] = input_type

    def set_response_options(self, response_options):
        self.schema["responseOptions"] = response_options
