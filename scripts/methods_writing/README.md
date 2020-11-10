# _Armitage_  - BIDS Report NLG

Simple program for template-based natural language rendering of reports based on [BIDS](http://bids.neuroimaging.io/) neuroimaging data. 

## Getting Started

* Use a Python 3.6 distribution
* Install requirements (mainly Jinja2)
```
pip install requirements
```

## Running

Just run the _main.py_ file:
```
python main.py
```
The main file uses default values to auto-generate a report:

* _data/sample_meg.json_ - The default input file that follows BIDS standards.
* _renderedReportResults.txt_ - Default output file
* _base_report.tmp_ - Default top level parent Jinja2 template used as the root of the hierarchical rendering.

Running with a -t argument allows to render a specific template. For instance:
```
python main.py institution
```

Would only render the _institution.tmp_ sub-template:

```
The recordings were performed in the Stanford University, 450 Serra Mall, Stanford, CA 94305-2004, USA.
```

