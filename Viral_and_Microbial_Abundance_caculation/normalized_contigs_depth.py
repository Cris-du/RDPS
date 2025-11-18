#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse

def normalize_mag(input_file, output_file, reads_count):
    """
    对单个 MAG abundance 文件进行标准化计算
    输入文件需要包含表头，第二列为长度，第三列为 mean depth
    """
    multiplier = 100000000  # 固定常数

    results = []
    with open(input_file, "r") as f:
        header = next(f)  # 跳过第一行表头
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) < 3:
                continue
            seq_name = parts[0]
            mean_depth = parts[2]

            try:
                mean_depth = float(mean_depth)
                normalized = (mean_depth * multiplier) / reads_count
                normalized_str = f"{normalized:.20f}"
                results.append(f"{seq_name}\t{normalized_str}\n")
            except ValueError:
                print(f"Skipping invalid line: {line.strip()}")
                continue

    with open(output_file, "w") as out:
        out.writelines(results)

def main():
    parser = argparse.ArgumentParser(
        description="Normalize a single MAG abundance file by reads count."
    )
    parser.add_argument("-rc", "--readcount", type=float, required=True,
                        help="Total reads base count for this sample")
    parser.add_argument("-id", "--input", required=True,
                        help="Input MAG abundance TSV file")
    parser.add_argument("-o", "--output", required=True,
                        help="Output normalized abundance file")

    args = parser.parse_args()

    normalize_mag(args.input, args.output, args.readcount)

if __name__ == "__main__":
    main()
