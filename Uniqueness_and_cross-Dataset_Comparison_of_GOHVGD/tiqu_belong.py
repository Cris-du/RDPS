#!/usr/bin/env python3

import argparse

def main():
    parser = argparse.ArgumentParser(description="Map cluster member sequences to their sources using a sequence-to-source table.")
    parser.add_argument("-it", required=True, help="Input TSV: sequence_name<tab>source (mapping file)")
    parser.add_argument("-iv", required=True, help="Input TSV: rep_sequence<tab>seq1&seq2&seq3 (cluster file, tab-separated, members joined by '&')")
    parser.add_argument("-o", required=True, help="Output file: rep_sequence<tab>source1&source2...")
    args = parser.parse_args()

    # Step 1: Build sequence -> source mapping from -it file
    seq_to_source = {}
    with open(args.it, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 2:
                seq_name = parts[0]
                source = parts[1]
                seq_to_source[seq_name] = source
            # 如果只有1列，忽略（或可设为 unknown，这里按原逻辑忽略）

    # Step 2: Process cluster file (-iv) and map to sources
    with open(args.iv, 'r') as fin, open(args.o, 'w') as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 1:
                # Only rep sequence, no members
                fout.write(f"{parts[0]}\t\n")
                continue
            elif len(parts) >= 2:
                rep_seq = parts[0]
                member_str = parts[1]
                if not member_str:
                    fout.write(f"{rep_seq}\t\n")
                    continue

                # Split member sequences by '&'
                follow_seqs = member_str.split('&')
                sources = set()
                for fs in follow_seqs:
                    src = seq_to_source.get(fs, 'unknown')
                    sources.add(src)

                # Sort and join with '&'
                sources_str = '&'.join(sorted(sources))
                fout.write(f"{rep_seq}\t{sources_str}\n")

    print(f"Cluster source mapping saved to {args.o}")

if __name__ == "__main__":
    main()
