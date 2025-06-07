#!/usr/bin/env python3
import sys

current_tag = None
current_count = 0

for line in sys.stdin:
    try:
        tag, count = line.strip().split('\t')
        count = int(count)
    except ValueError:
        continue  # skip malformed lines

    if current_tag == tag:
        current_count += count
    else:
        if current_tag:
            print(f"{current_tag}\t{current_count}")
        current_tag = tag
        current_count = count

# print the last tag count
if current_tag:
    print(f"{current_tag}\t{current_count}")
