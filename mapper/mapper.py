#!/usr/bin/env python3
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    header = next(reader, None)  # Skip the header
    for row in reader:
        if len(row) >= 2:
            tag = row[1].strip()
            if tag:
                print(f"{tag}\t1")

if __name__ == "__main__":
    main()
