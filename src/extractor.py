import re
from datetime import datetime

from PyPDF2 import PdfReader

def get_text(file_path):
    reader = PdfReader(file_path)
    number_of_pages = len(reader.pages)
    text = '\n'.join([
        reader.pages[_].extract_text()
        for _ in range(number_of_pages)
    ])
    text = re.sub(r' *\xa0 *', ' ', text)
    return text


def get_conac(text):
    pattern = re.compile(r'(?<=conac\W)\d+', flags=re.I)
    return pattern.search(text).group(0)


def get_invoice_number(text):
    pattern = re.compile(r'(?<=invoice number\W)\d+', flags=re.I)
    return pattern.search(text).group(0)


def get_statement_date(text):
    pattern = re.compile(r'(?<=statement date\W)\d.+', flags=re.I)
    return pattern.search(text).group(0)

def get_bill_date_range(text):
    pattern = re.compile(r'(?<=your bill for\W)(\d.+\d)\W+to\W+(\d.+\d)', flags=re.I)
    match = pattern.search(text)
    return match.group(1), match.group(2)


def date_range_split(text):
    pattern = re.compile(r'(\d+ \w+)\W+(\d+ \w+ (\w+))', flags=re.I)
    match = pattern.search(text)
    start = match.group(1)
    end = match.group(2)
    year = match.group(3)
    start_full = ' '.join([start, year])
    return start_full, end


def get_previous_balance(text):
    pattern = re.compile(r'(?<=previous balance\W\$).+', flags=re.I)
    return pattern.search(text).group(0)


def get_energy_imported(text):
    pattern = re.compile(r'(?<=energy imported\W\$).+', flags=re.I)
    match = pattern.search(text)
    return match.group(0) if match else None


def get_energy_exported(text):
    pattern = re.compile(r'(?<=energy exported\W\$).+', flags=re.I)
    match = pattern.search(text)
    return match.group(0) if match else None


def get_total_amount_due(text):
    pattern = re.compile(r'(?<=please pay by\W)(\d+\W\w+\W\d+)\W+(.+)', flags=re.I)
    match = pattern.search(text)
    return match.group(1), match.group(2)


def get_broadband_charges(text):
    pattern = re.compile(r'(?<=Broadband charges\W\$).+', flags=re.I)
    match = pattern.search(text)
    return match.group(0) if match else None


def get_daily_charges(text):
    """
    Finds all "daily charge" entries and returns a list of tuples.
    Each tuple is (days, charge_per_day), e.g., [('30', '1.20'), ('2', '1.25')]
    """
    pattern = re.compile(r'(daily charge)\W+(\d+) days\W+([\d.]+?) dollars', flags=re.I)
    matches = pattern.findall(text)
    return matches if matches else []


def get_variable_charged(text):
    pattern = re.compile(r'(?:charged)\W+(.+) (\d+) kwh\W+(.+?) ', flags=re.I)
    matches = pattern.findall(text)
    return matches if matches else []


def get_no_charge(text):
    pattern = re.compile(r'(?:free)\W+(.+) (\d+) kwh\W+(.+?) ', flags=re.I)
    matches = pattern.findall(text)
    return matches if matches else []


def get_exported(text):
    pattern = re.compile(r'(.+)\W+(\d+) kwh\W+(-\d.+?) ', flags=re.I)
    matches = pattern.findall(text)
    return matches if matches else []


def get_fibre(text):
    pattern = re.compile(r'(.*fibre.*?) (\d+ \w+ - \d+ \w+ \d+) \$(.+)', flags=re.I | re.M)
    matches = pattern.findall(text)
    if matches:
        result = []
        for match in matches:
            fibre_item = match[0]
            fibre_range = match[1]

            fibre_start, fibre_end = date_range_split(fibre_range)
            fibre_start, fibre_end = get_date_key(fibre_start), get_date_key(fibre_end)

            fibre_price = match[2]
            result.append((fibre_item, fibre_start, fibre_end, fibre_price))
        return result
    return []


def get_date_key(date_str):
    """Converts a date string in the format 'dd mmm yyyy' to 'yyyymmdd' format.
    A piece of str, not dataframe."""

    try:
        x = datetime.strptime(date_str, '%d %b %Y')
        x = datetime.strftime(x, '%Y%m%d')
        return x
    except Exception as e:
        print(f"Error parsing date: {e}")
        return 19700101