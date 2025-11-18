#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) != 3:
    print("Usage: python fasta_length.py <input_fasta> <output_file>")
    sys.exit(1)

input_fa = sys.argv[1]
output_txt = sys.argv[2]

seq_name = None
seq_len = 0

with open(input_fa, "r") as infile, open(output_txt, "w") as outfile:
    for line in infile:
        line = line.rstrip("\n")

        if line.startswith(">"):
            # 如果已有上一个序列，先写出去
            if seq_name is not None:
                outfile.write(f"{seq_name}\t{seq_len}\n")

            # 保存完整序列名称（去掉第一个 ">"，其他全部保留）
            seq_name = line[1:]
            seq_len = 0

        else:
            seq_len += len(line.strip())

    # 最后一条序列写出
    if seq_name is not None:
        outfile.write(f"{seq_name}\t{seq_len}\n")
