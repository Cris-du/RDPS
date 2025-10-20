#!/usr/bin/env python3

import argparse
from collections import defaultdict

# 解析命令行参数
parser = argparse.ArgumentParser(description="Count the number of proteins for each virus in a .faa file")
parser.add_argument("-i", "--input", required=True, help="Input .faa file")
parser.add_argument("-o", "--output", required=True, help="Output file for virus protein counts")
args = parser.parse_args()

# 初始化字典来统计每个病毒的蛋白质数量
virus_counts = defaultdict(int)

# 处理输入文件
with open(args.input, 'r') as infile:
    for line in infile:
        if line.startswith(">"):  # 检测蛋白质序列标题行
            # 提取病毒蛋白名称并从中解析出病毒名称
            protein_name = line[1:].split(" # ")[0].strip()
            virus_name = "_".join(protein_name.split("_")[:-1])
            # 统计病毒名称
            virus_counts[virus_name] += 1

# 将结果输出到文件
with open(args.output, 'w') as outfile:
    # 输出表头
    outfile.write("VirusName\tProteinCount\n")
    # 输出统计结果
    for virus_name, count in virus_counts.items():
        outfile.write(f"{virus_name}\t{count}\n")

print(f"Protein counts per virus have been saved to {args.output}")
