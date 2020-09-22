from reproschema_schema import ReproschemaSchema


class ReproschemaItem(ReproschemaSchema):
    """
    class to deal with reproschema activities
    """

    def __init__(self):
        super().__init__()
        self.schema["@type"] = "reproschema:Field"
        self.schema["ui"] = {"inputType": []}
        self.schema["question"] = {}
        self.schema["responseOptions"] = {}
        # default input type is "char"
        self.set_input_type_as_char()

    def set_URI(self, URI):
        self.URI = URI

    def set_defaults(self, name):
        self._ReproschemaSchema__set_defaults(name)  # this looks wrong
        self.schema_file = name
        self.schema["@id"] = name
        self.set_input_type_as_char()

    def set_question(self, question, lang="en"):
        self.schema["question"][lang] = question

    def set_input_type(self, input_type):
        self.schema["ui"]["inputType"] = input_type

    def set_response_options(self, response_options):
        self.schema["responseOptions"] = response_options

    def set_input_type_as_radio(self, response_options):
        self.set_input_type("radio")
        self.set_response_options(response_options)

    def set_input_type_as_select(self, response_options):
        self.set_input_type("select")
        self.set_response_options(response_options)

    def set_input_type_as_char(self):
        self.set_input_type("text")
        self.set_response_options({"valueType": "xsd:string"})

    def set_input_type_as_int(self):
        self.set_input_type("number")
        self.set_response_options({"valueType": "xsd:integer"})

    def set_input_type_as_float(self):
        self.set_input_type("float")
        self.set_response_options({"valueType": "xsd:float"})

    def set_input_type_as_time_range(self):
        self.set_input_type("timeRange")
        self.set_response_options({"valueType": "datetime"})

    def set_input_type_as_slider(self):
        self.set_input_type_as_char()  # until the slide item of the ui is fixed
        # self.set_input_type("slider")
        # self.set_response_options({"valueType": "xsd:string"})

    def set_input_type_as_date(self):
        self.set_input_type("date")
        self.set_response_options({"valueType": "xsd:date"})

    # TODO
    # multitext: MultiTextInput/MultiTextInput.vue
    # email: EmailInput/EmailInput.vue
    # audioCheck: AudioCheck/AudioCheck.vue
    # audioRecord: WebAudioRecord/Audio.vue
    # audioPassageRecord: WebAudioRecord/Audio.vue
    # audioImageRecord: WebAudioRecord/Audio.vue
    # audioRecordNumberTask: WebAudioRecord/Audio.vue
    # audioAutoRecord: AudioCheckRecord/AudioCheckRecord.vue
    # year: YearInput/YearInput.vue
    # selectLanguage: SelectInput/SelectInput.vue
    # selectCountry: SelectInput/SelectInput.vue
    # selectState: SelectInput/SelectInput.vue
    # documentUpload: DocumentUpload/DocumentUpload.vue
    # save: SaveData/SaveData.vue
    # static: Static/Static.vue
    # StaticReadOnly: Static/Static.vue

    def set_basic_response_type(self, response_type):

        # default (also valid for "char" input type)
        self.set_input_type_as_char()

        if response_type == "int":
            self.set_input_type_as_int()

        # response is float
        elif response_type == "float":
            self.set_input_type_as_float()

        # response is date
        elif response_type == "date":
            self.set_input_type_as_date()

        # response is time range
        elif response_type == "time range":
            self.set_input_type_as_time_range()

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
