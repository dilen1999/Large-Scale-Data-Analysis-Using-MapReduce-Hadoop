#!/usr/bin/env python3
import sys

def main():
    current_question = None
    current_count = 0

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        question_id, count = line.split('\t')
        count = int(count)

        if current_question == question_id:
            current_count += count
        else:
            if current_question is not None:
                print(f"{current_question}\t{current_count}")
            current_question = question_id
            current_count = count

    # Print the last question's count
    if current_question is not None:
        print(f"{current_question}\t{current_count}")

if __name__ == "__main__":
    main()
