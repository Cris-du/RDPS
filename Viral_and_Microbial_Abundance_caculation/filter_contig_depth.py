#!/usr/bin/env python3
import argparse

def read_coverage_data(coverage_path):
    """ 从文件中读取序列名，并返回一个序列名集合 """
    qualified_sequences = set()
    with open(coverage_path, 'r') as file:
        for line in file:
            sequence_name = line.strip()
            qualified_sequences.add(sequence_name)
    return qualified_sequences

def filter_depth_data(depth_path, qualified_sequences, output_path):
    """逐行读取深度文件，保留包含在qualified_sequences集合中的序列及其相关数据，并输出到新文件中"""
    with open(depth_path, 'r') as infile, open(output_path, 'w') as outfile:
        header = infile.readline()  # 读取并写入表头
        outfile.write(header)
        for line in infile:
            sequence_name = line.strip().split()[0]
            if sequence_name in qualified_sequences:
                outfile.write(line)

def main():
    parser = argparse.ArgumentParser(description="Filter sequences based on sequence names.")
    parser.add_argument("-ic", "--input_coverage", required=True, help="Input file with sequence names")
    parser.add_argument("-id", "--input_depth", required=True, help="Input file with depth data")
    parser.add_argument("-o", "--output", required=True, help="Output file for filtered depth data")

    args = parser.parse_args()

    # Read coverage data and determine which sequences are qualified
    qualified_sequences = read_coverage_data(args.input_coverage)

    # Filter depth data based on qualified sequences and write to output file
    filter_depth_data(args.input_depth, qualified_sequences, args.output)

if __name__ == "__main__":
    main()
