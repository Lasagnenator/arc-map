"""
Uses the legacy Maxmind dataset for doing location lookups.
Dated 2016-Nov-05 from the wayback machine.
https://web.archive.org/web/20161105102242/http://dev.maxmind.com/geoip/legacy/geolite/
The page is no longer available on the internet and so the license requirement that comes with it can no longer be adequately met.

This product includes GeoLite data created by MaxMind, available from
<a href="http://www.maxmind.com">http://www.maxmind.com</a>.
"""

import ipaddress
import csv
import bisect
import iso3166

def row_to_entry(row):
    return {
        "start": int(row[2]), # numerical representations. Not standard form.
        "end": int(row[3]),
        "CC": row[4]
    }

with open("GeoIPCountryWhois.csv", "r") as f:
    data = sorted(map(row_to_entry, csv.reader(f)), key=lambda r:r["start"])

def lookup(ip):
    if "." in str(ip):
        # Normal IPv4 format, convert to numerical
        ip = int(ipaddress.ip_address(ip))
    else:
        ip = int(ip)

    index = bisect.bisect(data, ip, key=lambda r:r["start"]) - 1
    return iso3166.convert_2_to_3(data[index]["CC"])
