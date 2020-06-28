import pandas as pd
from sodapy import Socrata
from config import data_portal_url, keywords, set_names, app_token
import datetime
import os
import sys

# Initialize Socrata data connection
client = Socrata(data_portal_url, app_token)
ds = client.datasets()

# Use imported list of selected data sets; if empty, default to everything
if set_names is None:
    set_names = [d['resource']['name'] for d in ds]

resource_ids = {d['resource']['name']: d['resource']['id']  for d in ds}
sets =         {d['resource']['id']: d['resource']          for d in ds}

# Adjust the width of the text output
max_length = max([len(k) for k in keywords])
width = max_length + 4

# Create export folder if it does not exist
today = datetime.datetime.now().strftime('%Y%m%d')
try:
    folder = sys.argv[1]
    path = f'exports/{folder}/{today}'
except:
    path = f'exports/{today}'

path_check = '.'
for dir in path.split('/'):
    path_check += f'/{dir}'
    if not os.path.isdir(path_check):
        os.mkdir(path_check)


def describe_set(id:str) ->str:
    msg = f"\nDataset: {sets[id]['name']}"
    msg += f"\nResource_id: {id}"
    msg += f"\nLast updated: {sets[id]['updatedAt']}"
    msg += f"\n\nDescription: {sets[id]['description']}"
    msg += f"\n\nColumns: "

    field_width = max([len(f) for f in sets[id]['columns_field_name']]) + 4

    for counter, value in enumerate(sets[id]['columns_field_name']):
        padding = field_width - len(value)
        msg+=f"\n   {value}{' '* padding}: {sets[id]['columns_datatype'][counter]}"
    return msg


def export_frame(kf, set_name):
    # Don't include dictionaries while checking for duplicates
    columns = list(kf.columns)
    exclude = []

    for c in columns:
        for d in kf[c].dropna().values.tolist():
            if type(d) == dict:
                exclude.append(c)
                break

    subset = [c for c in columns if c not in exclude]
    kf = kf.drop_duplicates(subset=subset)

    set_name=set_name.replace('/', '_')
    kf.to_excel(f'{path}/{set_name}.xlsx', index=False)
    return len(kf)


def main():

    # Capture output to a log
    with open(f"{path}/log.txt", "w+") as log:
        for s in set_names:

            # For each data set, get the resource id and reset the dataframe
            resource = resource_ids.get(s)
            kf = None

            msg = f'\nChecking {s} for keywords:\n'
            print(msg, end='')
            log.write(msg)

            try:
                for k in keywords:
                    results = client.get(resource, q=k)
                    df = pd.DataFrame.from_records(results)

                    padding = ' ' * (width - len(k))
                    msg = f'{k}{padding}{len(results)} results\n'
                    print(msg, end='')
                    log.write(msg)

                    # If there's already some data, append new results; otherwise make a dataframe
                    if len(results) > 0:
                        if kf is not None:
                            kf = kf.append(df, sort=True)
                        else:
                            kf = df

            except Exception as e:
                msg = f'Error checking dataset: {e}\n'
                print(msg)
                log.write(msg)
                continue

            if kf is not None:
                unique = export_frame(kf, s)
                msg = f"Duplicates removed, exported {unique} unique records. \n"
                print(msg)
                log.write(msg)

                with open(f"{path}/resource_descriptions.txt", "a+") as rd:
                    rd.write('\n\n'+'-'*125+'\n')
                    rd.write(describe_set(resource))

        msg = "\nNo further data sets."
        print(msg)
        log.write(msg)


main()


