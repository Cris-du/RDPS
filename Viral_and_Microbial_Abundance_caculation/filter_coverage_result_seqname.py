#!/usr/bin/env python3
import argparse

def filter_sequences(input_path, output_path, coverage_threshold):
    """从TSV文件中筛选覆盖率高于阈值的序列名称，并将其写入输出文件"""
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            parts = line.strip().split('\t')  # 使用'\t'作为分隔符
            if float(parts[6]) > coverage_threshold:
                outfile.write(parts[0] + '\n')  # 写入序列名称，后跟换行符

def main():
    parser = argparse.ArgumentParser(description="Filter sequences by coverage threshold from a TSV file.")
    parser.add_argument("-i", "--input", required=True, help="Input TSV file with sequence data and coverage")
    parser.add_argument("-o", "--output", required=True, help="Output file for storing qualified sequence names")
    parser.add_argument("-c", "--coverage", type=float, required=True, help="Coverage threshold value")

    args = parser.parse_args()

    # 调用筛选函数
    filter_sequences(args.input, args.output, args.coverage)

if __name__ == "__main__":
    main()
