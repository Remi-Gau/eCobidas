def convert_to_str(df_field):

    return df_field.tolist()[0]


def convert_to_int(df_field):

    return int(df_field.tolist()[0])

def snake_case(input):

    return input.lower().replace("\n", "").replace(" ", "_")