#!/usr/bin/env python3
import sys

def main():
    current_tag = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        tag, count = line.split('\t', 1)
        try:
            count = int(count)
        except ValueError:
            continue

        if current_tag == tag:
            current_count += count
        else:
            if current_tag:
                print(f"{current_tag}\t{current_count}")
            current_tag = tag
            current_count = count

    if current_tag == tag:
        print(f"{current_tag}\t{current_count}")

if __name__ == "__main__":
    main()
