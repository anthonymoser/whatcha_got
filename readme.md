## Whatcha Got
is a tool for doing broad searches of data portals running on the Socrata platform.
Just supply a list of keywords and a data portal url, and it will search all available datasets for each of the keywords;
each dataset will generate a spreadsheet of results, with duplicates removed.

### Setup
1. You'll need to install Python 3.7 or greater.
2. It has only two dependencies: sodapy (a Python library for interacting with Socrata) and Pandas. You can install them
using pip, or pipenv.
3. Rename `config_example.py` to `config.py`
4. Update config.py with the URL of the data portal.
5. Optional setup: create a Socrata user account and get an app key

### Usage
Just put a list of keywords in config.py and run\
`python whatcha_got.py [optional folder name]`

When you run the program it will create a folder called Exports. You can specify a subfolder name in case you want to
organize your searches around different topics. 

## Output
The output will go in Exports/[optional folder]/date. Output includes: 
- `log.txt` matches printed output. It contains which data sets were searched, how many results were found for each
keyword, and how many rows were output for each data set after removing duplicates. Data sets with no results do not
generate files.
- `resource_descriptions.txt` contains, for each exported data set\
-- Name\
-- Resource id\
-- Time Last Updated\
-- Description of data set\
-- List of field names and data types
- One .xlsx file for each data set that returned results. Combines results of all keywords, removing duplicates.

## Data Set Errors
Because this script searches all available datasets with string keywords, some that may not contain string fields will
return a 400 error `Bad Request. Invalid SoQL query`\
Other data sets may not be accessible for other reasons, such as endpoint timeout.

## Compatible Data
This script has been tested against Chicago's data portal, and texas.data.gov; in theory it should work on any Socrata
data portal. You can find many available data sets at [https://opendatanetwork.com](https://opendatanetwork.com)