# CONTRIBUTING

Make sure to also read the
[How to contribute section](https://remi-gau.github.io/eCobidas/80-how-to-contribute/).

## Requirements

You will need to have installed.

-   Python
-   [node.js](https://nodejs.org/en/)
-   [Git](https://git-scm.com/downloads)

If you are running Windows 10, you will want to work directly in a Linux Windows
sub-system.

An simple way to do this is to install
[Ubuntu from the Windows App store](https://www.microsoft.com/en-us/p/ubuntu-2004-lts/9n6svws3rx71).

### Python 3.8 or above

An easy way to install Python is to rely on
[Conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation)

If you are on Linux this should be enough:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

<!-- TODO
check if virtualenv is installed in base conda
-->

### node.js

A good way to To install javascript [`node.js`](https://nodejs.org/en/), is to
install [node version manager](https://github.com/nvm-sh/nvm) (NVM) to help you
deal with different version of `node.js`.

In a terminal or in Windows WSL2, you can install NVM by typing:

```
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
```

Then close your terminal and reopen it then run the following to install the
version 12 of `node.js` (using the latest version of `node.js` should be fine,
so this is more there as an example).

```
nvm install node
nvm install 12
```

## Set up

Fork and clone the repo. Preferably set up a python virtual environment.

Then run make install.

```
git clone https://github.com/YOUR_GITHUB_USERNAME/eCobidas.git
cd eCobidas
virtualenv -p python3.8 env
source env/bin/activate
make install
```

## Downloading the spreadsheet and converting them

A lot of recipe are already in the [Makefile](Makefile) to facilitate daily
work.

For example:

-   `make neurovault`
-   `make artemis`
-   `make pet`

Here is a description of the Neurovault recipe `make neurovault`.

```bash
# remove previous runs:
rm -rf inputs/csv/neurovault
rm -rf schemas/neurovault/

# use a bash script to download the spreadsheet
bash download_tsv.sh neurovault

# use the local ecobidas python package to convert the spreadsheet in jsonld
ecobidas_convert --schema neurovault

# make sure the jsonld are valid with some node.js and reproschema validation
grep -r  "@context" schemas/neurovault | cut -d: -f1 | xargs -I fname jsonlint -q fname
reproschema -l DEBUG validate schemas/neurovault
```

## Serving the local protocols and activities to test them with the reproschema-ui

```
python schemas/simple-cors-http-server.py
```

## Editing the spreadsheets

DO NOT EDIT THE DIRECTLY IN THE REPOSITORY!!!

Instead edit them on the google drive and use `download_tsv.sh` to download them
locally. Or type `make download_all` to download update all the spreadsheets.

## Visual studio code settings

Load the `ecobidas.code-workspace` file in the `.vscode` folder.

