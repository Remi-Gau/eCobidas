# CONTRIBUTING

## Requirements

-   python 3.7

## Set up

Fork and clone the repo. Preferably set up a python virtual environment. Then
run make install.

```
git clone https://github.com/YOUR_GITHUB_USERNAME/eCobidas.git
cd eCobidas
virtualenv -p python3.8 env
source env/bin/activate
make install
```



## Editing the spreadsheets

DO NOT EDIT THEM DIRECTLY !!!

Instead edit them on the google drive and use `download_tsv.sh` to download them
locally. Or type `make download_all` to download update all the spreadsheets.

## Visual studio code settings

Load the `ecobidas.code-workspace` file in the `.vscode` folder.
