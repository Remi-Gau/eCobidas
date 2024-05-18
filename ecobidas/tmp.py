import pandas as pd
from ruamel.yaml import YAML

# Create a simple DataFrame
df = pd.read_csv("ecobidas/inputs/spreadsheet_google_id.tsv", sep="\t")
# Setup ruamel.yaml instance
yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)
# Convert the DataFrame to YAML
yaml_data = df.to_dict(orient="records")
with open("ecobidas/inputs/spreadsheet_google_id.yml", "w") as f:
    yaml.dump(yaml_data, f)
