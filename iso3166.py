
import csv

def build_tables(data) -> dict[str, dict[str, dict[str, str]]]:
    keys = list(data[0].keys())
    tables = {k: {} for k in keys}
    for entry in data:
        for k, table in tables.items():
            table[entry[k]] = entry
    # tables[key][code] = {name, 2letter, 3letter, code}
    return tables

with open("iso3166.tsv", "r") as f:
    data = build_tables(list(csv.DictReader(f, delimiter="\t")))

def convert_2_to_3(code: str):
    return data["2letter"][code]["3letter"]

def convert_3_to_2(code: str):
    return data["3letter"][code]["2letter"]

def exists(code):
    return any(code in table.keys() for table in data.values())
