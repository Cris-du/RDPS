#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description="Filter alignment file based on protein count and alignment percentage.")
    parser.add_argument("-i1", required=True, help="Input file 1: QueryVirus<tab>ProteinCount (with header)")
    parser.add_argument("-i2", required=True, help="Input file 2: QueryVirus<tab>TargetVirus<tab>AlignmentPct (with header)")
    parser.add_argument("-o", required=True, help="Output filtered TSV file")
    args = parser.parse_args()

    # Step 1: Read file 1 to get query viruses with protein count >= 5
    query_viruses_with_enough_proteins = set()
    with open(args.i1, 'r') as f1:
        header = True
        for line in f1:
            if header:
                header = False
                continue
            parts = line.strip().split('\t')
            if len(parts) < 2:
                continue
            virus = parts[0]
            try:
                count = int(parts[1])
            except ValueError:
                continue  # skip malformed lines
            if count >= 5:
                query_viruses_with_enough_proteins.add(virus)

    # Step 2: Filter file 2
    with open(args.i2, 'r') as f2, open(args.o, 'w') as out:
        header = True
        for line in f2:
            if header:
                out.write(line)  # write original header
                header = False
                continue

            parts = line.strip().split('\t')
            if len(parts) < 3:
                continue

            query_virus = parts[0]
            try:
                pct = float(parts[2])
            except ValueError:
                continue  # skip malformed percentage

            # Apply both filters: pct >= 50 AND query virus has >=5 proteins
            if pct >= 50 and query_virus in query_viruses_with_enough_proteins:
                out.write(line)

    print(f"Filtered results saved to {args.o}")

if __name__ == "__main__":
    main()
