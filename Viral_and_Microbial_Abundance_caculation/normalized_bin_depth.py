#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def normalize_mag(input_file, output_file, reads_count):
    """
    对只有两列 (contig, mean_depth) 的 MAG abundance 文件进行标准化。
    自动跳过表头。
    去除 mean_depth = 0 的行。
    """
    multiplier = 10  # 固定常数

    results = []
    with open(input_file, "r") as f:
        header = next(f)  # 跳过表头
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue

            seq_name = parts[0]
            mean_depth = parts[1]

            try:
                mean_depth = float(mean_depth)
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
                continue

            # 跳过 mean_depth = 0 的 contig
            if mean_depth == 0:
                continue

            # 标准化计算
            normalized = (mean_depth * multiplier) / reads_count
            normalized_str = f"{normalized:.20f}"

            results.append(f"{seq_name}\t{normalized_str}\n")

    # 输出结果
    with open(output_file, "w") as out:
        out.writelines(results)

def main():
    parser = argparse.ArgumentParser(
        description="Normalize a MAG abundance file with two columns (contig, mean_depth)."
    )
    parser.add_argument("-rc", "--readcount", type=float, required=True,
                        help="Total reads base count for this sample.")
    parser.add_argument("-id", "--input", required=True,
                        help="Input MAG abundance TSV file.")
    parser.add_argument("-o", "--output", required=True,
                        help="Output normalized abundance file.")

    args = parser.parse_args()

    normalize_mag(args.input, args.output, args.readcount)

if __name__ == "__main__":
    main()
