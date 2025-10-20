#!/usr/bin/env python3

import argparse

# 解析输入参数
parser = argparse.ArgumentParser(description="Filter B file based on protein count in A file.")
parser.add_argument("-i1", "--input1", required=True, help="Input file A with virus names and total proteins.")
parser.add_argument("-i2", "--input2", required=True, help="Input file B with virus match percentages.")
parser.add_argument("-o", "--output", required=True, help="Output file to save filtered results.")
args = parser.parse_args()

# 读取A文件，将每个查询病毒及其蛋白质总数存储在字典中（仅保留蛋白质总数>=5的病毒）
virus_protein_totals = {}
with open(args.input1, 'r') as file_a:
    next(file_a)  # 跳过表头
    for line in file_a:
        parts = line.strip().split('\t')
        query_virus = parts[0]
        total_proteins = int(parts[1])
        
        # 仅保留蛋白质总数大于等于5的查询病毒
        if total_proteins >= 5:
            virus_protein_totals[query_virus] = total_proteins

# 打开输出文件并写入表头
with open(args.output, 'w') as output_file:
    output_file.write("QueryVirus\tTargetVirus\tPercentage\n")
    
    # 读取B文件，检查每一行的查询病毒是否在符合条件的字典中
    with open(args.input2, 'r') as file_b:
        next(file_b)  # 跳过表头
        for line in file_b:
            parts = line.strip().split('\t')
            query_virus = parts[0]
            target_virus = parts[1]
            percentage = parts[2]
            
            # 如果查询病毒在字典中（即符合蛋白质总数>=5的条件），则将该行写入输出文件
            if query_virus in virus_protein_totals:
                output_file.write(f"{query_virus}\t{target_virus}\t{percentage}\n")
