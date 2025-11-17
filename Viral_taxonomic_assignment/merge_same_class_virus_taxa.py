#!/usr/bin/env python3

import csv
import argparse

def main():
    parser = argparse.ArgumentParser(description="Merge virus taxonomy rows by virus name, keeping lowest unambiguous classification level.")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file with virus taxonomy (first column: virus name)")
    parser.add_argument("-o", "--output", required=True, help="Output TSV file with merged taxonomy")
    args = parser.parse_args()

    with open(args.input, 'r', newline='') as infile, open(args.output, 'w', newline='') as outfile:
        reader = csv.reader(infile, delimiter='\t')
        writer = csv.writer(outfile, delimiter='\t')

        # Read and write header
        header = next(reader)
        writer.writerow(header)

        # Group rows by virus name
        virus_classifications = {}
        for row in reader:
            if not row:  # skip empty lines
                continue
            virus_name = row[0]
            classification = row[1:]
            if virus_name in virus_classifications:
                virus_classifications[virus_name].append(classification)
            else:
                virus_classifications[virus_name] = [classification]

        # Process each virus
        for virus_name, classifications in virus_classifications.items():
            num_cols = len(classifications[0])
            merged = [''] * num_cols

            # Go column by column (from high to low taxonomic rank)
            for i in range(num_cols):
                values = set()
                total = len(classifications)
                non_empty = 0

                for cls in classifications:
                    val = cls[i].strip() if i < len(cls) else ''
                    if val != '':
                        values.add(val)
                        non_empty += 1

                # If all non-empty values are identical AND all rows have a value (no missing)
                if len(values) == 1 and non_empty == total:
                    merged[i] = list(values)[0]
                else:
                    # As soon as ambiguity or missing data appears, stop and leave rest blank
                    break

            writer.writerow([virus_name] + merged)

    print(f"Merged taxonomy saved to {args.output}")

if __name__ == "__main__":
    main()
