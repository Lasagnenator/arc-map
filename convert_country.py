
import csv
import json
from collections import defaultdict
import iso3166

def row_to_entry(row: list[str], order: list[int]):
    name = row[order[0]].upper()
    if len(name) == 2:
        # make it 3 letter
        name = iso3166.convert_2_to_3(name)
    # make sure it exists
    assert iso3166.exists(name), row

    obj = {
        "name": name,
        "lat": float(row[order[1]]),
        "long": float(row[order[2]])
    }
    return obj

def rows_to_map(rows: list[dict[str,str]]) -> dict[str, list[str]]:
    data = defaultdict(list)
    for row in rows:
        data[row["name"]].append({"lat":row["lat"], "long":row["long"]})

    return data

def join_maps(maps) -> dict[str, list[str]]:
    data = defaultdict(list)
    for map in maps:
        for name in map.keys():
            data[name].extend(map[name])

    # deduplicate
    for k in data.keys():
        data[k] = [dict(t) for t in {tuple(d.items()) for d in data[k]}]

    return data

def read(file, order, sep=","):
    with open(file, "r") as f:
        next(f)
        data = list(map(lambda row: row_to_entry(row, order), csv.reader(f, delimiter=sep)))
        data = rows_to_map(data)
    return data

# filename, [country name, latitude, longitude], separator
maps = [
    #read("cnlatlong.csv", [2,1,0]),
    read("country_latlon.csv", [0,1,2]),
    read("country_centroids_primary.tsv", [12, 0, 1], "\t"),
    read("samplatlong.csv", [2,1,0]),
]

data = join_maps(maps)

picker = """

// Get a random coordinate from this country.
function cn_to_coord(name) {
    count = cnlatlong[name].length;
    choice = Math.floor(Math.random() * count);
    return cnlatlong[name][choice];
};
"""

with open("cnlatlong.js", "w") as f:
    f.write("cnlatlong = ")
    json.dump(data, f, sort_keys=True, indent=None, separators=(',', ':'))
    f.write(";")
    f.write(picker)
