import os
import re
from collections import defaultdict

import pandas as pd
from pandas import json_normalize

from src.extractor import *


RAW = os.path.join('.', 'data', 'raw')
PROCESSED = os.path.join('.', 'data', 'processed')

# ideally, you only put relevant files in the RAW directory
# regardless, if the files are in a subdirectory, this pattern will match
PATH_PATTERN = re.compile(r'(.*202[\d])\Wcontactbill.pdf', flags=re.I)


def walk():
    """Walks through the RAW directory and yields tuples of (date, file_path)
    where date is extracted from the filename.
    """
    for root, _, files in os.walk(RAW):
        for filename in files:
            if PATH_PATTERN.search(filename):
                match = PATH_PATTERN.search(filename)
                a_date = match.group(1)
                file_path = os.path.join(root, filename)
                yield a_date, file_path


def process_file(file_path):

    text = get_text(file_path)

    data = {}
    data['invoice_num'] = get_invoice_number(text)

    data['basics'] = {
        'conac': get_conac(text),
        'bill_date_range_start': get_date_key(
            get_bill_date_range(text)[0]
            ),
        'bill_date_range_end': get_date_key(
            get_bill_date_range(text)[1]
            ),
        'statement_date': get_date_key(get_statement_date(text)),
        'energy_imported': get_energy_imported(text),
        'energy_exported': get_energy_exported(text),
        'broadband_charges': get_broadband_charges(text),
    }

    daily_charges = get_daily_charges(text)
    if daily_charges:
        data['daily_charges'] = [
            {
                'item': item,
                'days_charged': days,
                'daily_charge': charge
                }
            for item, days, charge in daily_charges
        ]   

    variable_charged = get_variable_charged(text)
    if variable_charged:
        data['variable_charged'] = [
            {
                'item': item,
                'unit': unit,
                'price': price
                }
            for item, unit, price in variable_charged
        ]
    
    fibre = get_fibre(text)
    if fibre:
        data['fibre'] = [
            {
                'item': item,
                'date_range_start': start,
                'date_range_end': end,
                'price': price,
                }
            for item, start, end, price in fibre
        ]
    
    exported = get_exported(text)
    if exported:
        data['exported'] = [
            {
                'item': item,
                'unit': unit,
                'price': price
                }
            for item, unit, price in exported
        ]
    
    no_charge = get_no_charge(text)
    if no_charge:
        data['no_charge'] = [
            {
                'no_charge_item': item,
                'no_charge_unit': unit,
                'no_charge_price': price
                }
            for item, unit, price in no_charge
        ]

    return data  # which is a dictionary with all the extracted data


def get_dfs():

    # both nested and non-nested fields will be converted to dataframes
    # and stored under their respective keys
    dfs = defaultdict(list)

    # might be useful to include file path (_) for traceability
    for _, file_path in walk():

        try:
            x = process_file(file_path)
            non_nested_fields = x.pop('basics')
            non_nested_fields['invoice_num'] = x['invoice_num']

            for k, v in x.items():

                if isinstance(v, list):
                    df = json_normalize(
                        data=x,
                        record_path=[k],
                        meta=['invoice_num']
                    )
                    dfs[k].append(df)

                else:
                    non_nested_fields[k] = v # remove the processed key from x

            dfs['basics'].append(pd.DataFrame([non_nested_fields]))

        except Exception as e:
            print(f"Error processing {file_path}: {e}\n")
            continue
    
    return dfs

def main():

    dfs = get_dfs()
    dfs = {k: pd.concat(v, ignore_index=True) for k, v in dfs.items()}
    
    for k, v in dfs.items():
        print(f"Processing {k} with {len(v)} dataframes.")
        print(v)
        v.to_csv(f'{PROCESSED}/fact_contact_energy_bill_{k}.csv', index=None)


if __name__ == "__main__":
    main()