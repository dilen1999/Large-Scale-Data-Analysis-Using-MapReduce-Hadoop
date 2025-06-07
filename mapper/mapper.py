#!/usr/bin/env python3
import sys
import csv

for line in sys.stdin:
    try:
        row = next(csv.reader([line]))
        tag = row[1]  # assuming the second column contains the tag
        print(f"{tag}\t1")
    except Exception:
        continue  # skip malformed lines
