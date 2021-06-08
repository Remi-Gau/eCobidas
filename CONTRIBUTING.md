# CONTRIBUTING

## Virtural environment

```bash
virtualenv -p python3.8 env
source env/bin/activate
pip install -r requirements.txt
```

## Install the "dev" version of reproschema

```bash
# clone Rémi's fork of Reproschema on your machine
git clone https://github.com/Remi-Gau/reproschema-py.git  /home/remi/github
# checkout the "dev" branch
cd /home/remi/github/reproschema-py
git checkout remi_schema_creator
# pip install it
pip install -e /home/remi/github/reproschema-py
```
## Notes

Using then `pip freeze` should give you this with the specific shasum of the
commit between the `@` and the `#`:

```
-e git+https://github.com/Remi-Gau/reproschema-py.git@122a5f69ef8580752dc13c251db81cbf5fb137ee#egg=reproschema
```

Aaaaaaaaaannnnnnnnndd this does not work!!! Doing an `import` gives me package
or module unknow...

Maybe one day I will understand how Python path and import work...

OK So brute force approach is that once cloned and the correct branch checked
out, the I update the path of Python to force it look into the relevant folder
by adding the following in my code...

```python
import os, sys 
my_path = os.path.dirname("/home/remi/github/reproschema-py/reproschema/models/")
sys.path.insert(0, my_path)
```

I can then do:
```python
from models import Item
```



## Visual studio code settings

Load the `ecobidas.code-workspace` file in the `.vscode` folder.
