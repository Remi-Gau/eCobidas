def return_protocol_details(protocol_name_to_return):
    """
    Describes each spreadsheet: a sort of data dictionnary that should be turned 
    into an json in the long run but being lazy for now.
    Refactoring one step at a time.
    """

    # Neurovaut
    if protocol_name_to_return.lower() == "neurovault":

        CSV_INFO = {
            "section": {"col": 4, "name": "activity"},
            "act_pref_label": {"col": 5, "name": "activity_pref_label"},
            "item": {"col": 6, "name": "item"},
            "question": {"col": 9, "name": "question"},
            "resp_type": {"col": 11, "name": "field_type"},
            "choice": {"col": 12, "name": "choices"},
            "mandatory": {"col": 7, "name": "mandatory"},
            "include": {"col": 3, "name": "include"},
            "vis": {"col": 8, "name": "visibility"},
            "preamble": {"col": 10, "name": "details"},
        }

    # PET
    if protocol_name_to_return.lower() == "pet":

        CSV_INFO = {
            "section": {"col": 7, "name": "activity"},
            "act_pref_label": {"col": 8, "name": "activity_pref_label"},
            "item": {"col": 9, "name": "item"},
            "question": {"col": 12, "name": "question"},
            "resp_type": {"col": 14, "name": "field_type"},
            "choice": {"col": 15, "name": "choices"},
            "mandatory": {"col": 10, "name": "mandatory"},
            "include": {"col": 6, "name": "include"},
            "vis": {"col": 11, "name": "visibility"},
            "preamble": {"col": 13, "name": "details"},
        }

    # COBIDAS MRI
    if protocol_name_to_return.lower() == "mri":

        CSV_INFO = {
            "section": {"col": 6, "name": "activity"},
            "act_pref_label": {"col": 7, "name": "activity_pref_label"},
            "item": {"col": 13, "name": "item"},
            "question": {"col": 17, "name": "question"},
            "resp_type": {"col": 19, "name": "field_type"},
            "choice": {"col": 20, "name": "choices"},
            "mandatory": {"col": 15, "name": "mandatory"},
            "include": {"col": 3, "name": "include"},
            "vis": {"col": 21, "name": "visibility"},
            "preamble": {"col": 18, "name": "details"},
        }

    # COBIDAS eyetracker
    if protocol_name_to_return.lower() == "eyetracker":

        CSV_INFO = {
            "include": {"col": 6, "name": "include"},
            "section": {"col": 7, "name": "activity"},
            "act_pref_label": {"col": 8, "name": "activity_pref_label"},
            "act_descrip": {"col": 9, "name": "activity_descrip"},
            "item": {"col": 10, "name": "item"},
            "item_pref_label": {"col": 11, "name": "item_pref_label"},
            "item_descrip": {"col": 12, "name": "item_descrip"},
            "question": {"col": 15, "name": "question"},
            "resp_type": {"col": 17, "name": "field_type"},
            "choice": {"col": 18, "name": "choices"},
            "mandatory": {"col": 13, "name": "mandatory"},
            "vis": {"col": 14, "name": "visibility"},
            "preamble": {"col": 16, "name": "details"},
        }

    return CSV_INFO
