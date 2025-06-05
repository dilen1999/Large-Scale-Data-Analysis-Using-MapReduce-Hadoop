#!/usr/bin/env python3
import sys
import csv

def main():
    try:
        reader = csv.DictReader(sys.stdin)
        for row in reader:
            parent_id = row.get('ParentId')
            if parent_id:
                print(f"{parent_id}\t1")
    except Exception:
        pass  # Skip lines that can't be parsed

if __name__ == "__main__":
    main()
