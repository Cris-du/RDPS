#!/usr/bin/env python3

import argparse
from collections import defaultdict

# 解析命令行参数
parser = argparse.ArgumentParser(description="Count UNIQUE query proteins from each virus that match to a target virus")
parser.add_argument("-i", "--input", required=True, help="Input TSV file without header (qprotein\ttprotein)")
parser.add_argument("-o", "--output", required=True, help="Output TSV: QueryVirus, TargetVirus, UniqueProteinCount")
args = parser.parse_args()

# 使用 defaultdict(set) 来自动去重每个 (query_virus, target_virus) 对应的 query proteins
matches = defaultdict(lambda: defaultdict(set))

# 处理输入文件
with open(args.input, 'r') as infile:
    for line in infile:
        fields = line.strip().split("\t")
        if len(fields) < 2:
            continue
        
        query_protein = fields[0]
        target_protein = fields[1]

        # 提取病毒名（保持原规则）
        query_virus = "_".join(query_protein.split("_")[:-1])
        target_virus = target_protein.split("_prot_")[0]

        # 将 query_protein 添加到对应 (query_virus, target_virus) 的集合中（自动去重）
        matches[query_virus][target_virus].add(query_protein)

# 输出结果
with open(args.output, 'w') as outfile:
    outfile.write("QueryVirus\tTargetVirus\tUniqueQueryProteinCount\n")
    
    for query_virus in sorted(matches.keys()):
        for target_virus in sorted(matches[query_virus].keys()):
            count = len(matches[query_virus][target_virus])  # 去重后的蛋白数量
            outfile.write(f"{query_virus}\t{target_virus}\t{count}\n")

print(f"Unique query protein counts per virus pair have been saved to {args.output}")