from ..create_schema import return_protocol_details

input_file, csv_info = return_protocol_details("test_data")

print(input_file)
print(csv_info)