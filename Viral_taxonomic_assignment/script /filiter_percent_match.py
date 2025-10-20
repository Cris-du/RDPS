#!/usr/bin/env python3

import argparse

# 解析输入参数
parser = argparse.ArgumentParser(description="Filter rows based on percentage threshold.")
parser.add_argument("-i", "--input", required=True, help="Input file with percentage data.")
parser.add_argument("-o", "--output", required=True, help="Output file to save filtered results.")
args = parser.parse_args()

# 打开输出文件并写入带表头的结果
with open(args.output, 'w') as output_file:
    # 读取输入文件
    with open(args.input, 'r') as input_file:
        # 读取表头并写入到输出文件
        header = input_file.readline()
        output_file.write(header)
        
        # 处理每一行数据
        for line in input_file:
            parts = line.strip().split('\t')
            query_virus = parts[0]
            target_virus = parts[1]
            percentage = float(parts[2])
            
            # 判断百分比是否大于等于50，并写入符合条件的行
            if percentage >= 50:
                output_file.write(line)
