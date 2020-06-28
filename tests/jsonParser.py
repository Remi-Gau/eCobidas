import os
import json

tested = 0
for root, dirs, files in os.walk('activities', topdown=True):
    for name in files:
        filename = os.path.join(root, name)
        with open(filename) as fp:
            try:
                tested +=1
                data = json.load(fp)
                if data["@id"] and data["@id"] != name:
                    raise ValueError(f"{root}/{name} does not have matching @id")
            except json.decoder.JSONDecodeError:
                print(f"{root}/{name} could not be loaded")
                raise
if tested == 0:
    raise ValueError("Zero files tested")

