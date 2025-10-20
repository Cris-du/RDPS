#!/usr/bin/env python3

import argparse

# 解析输入参数
parser = argparse.ArgumentParser(description="Calculate protein match percentage for viruses.")
parser.add_argument("-i1", "--input1", required=True, help="Input file A with virus names and total proteins.")
parser.add_argument("-i2", "--input2", required=True, help="Input file B with virus match details.")
parser.add_argument("-o", "--output", required=True, help="Output file to save results.")
args = parser.parse_args()

# 读取A文件，将每个查询病毒及其蛋白质总数存储在字典中
virus_protein_totals = {}
with open(args.input1, 'r') as file_a:
    next(file_a)  # 跳过表头
    for line in file_a:
        parts = line.strip().split('\t')
        query_virus = parts[0]
        total_proteins = int(parts[1])
        virus_protein_totals[query_virus] = total_proteins

# 打开输出文件以保存结果
with open(args.output, 'w') as output_file:
    # 写入表头
    output_file.write("QueryVirus\tTargetVirus\tPercentage(%)\n")
    
    # 读取B文件，计算匹配蛋白质数量的百分比并写入输出文件
    with open(args.input2, 'r') as file_b:
        next(file_b)  # 跳过表头
        for line in file_b:
            parts = line.strip().split('\t')
            query_virus = parts[0]
            target_virus = parts[1]
            matched_proteins = int(parts[2])
            
            # 计算百分比
            if query_virus in virus_protein_totals:
                total_proteins = virus_protein_totals[query_virus]
                percentage = (matched_proteins / total_proteins) * 100
                
                # 写入结果，格式：查询病毒\t目标病毒\t百分比
                output_file.write(f"{query_virus}\t{target_virus}\t{percentage:.2f}\n")
