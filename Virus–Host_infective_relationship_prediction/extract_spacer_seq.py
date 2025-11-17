#!/usr/bin/env python3

import argparse

def extract_spacers_to_fasta(file_path, output_file_path):
    organism = ""
    crispr_count = 0
    spacers = []  # 初始化一个空列表，用来暂存找到的spacer序列及其信息

    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('ORGANISM:'):
                organism = line.split('ORGANISM:')[1].strip().replace(' ', '_').replace(',', '')
            elif 'CRISPR' in line and 'Range:' in line:
                crispr_count += 1
            elif line.strip() and not line.startswith('Bases:') and '[' in line:
                parts = line.strip().split('\t')
                if len(parts) >= 4:  # 确保有足够的部分来提取SPACER序列
                    spacer_sequence = parts[3].strip()
                    if spacer_sequence:  # 确保SPACER序列不为空
                        start_pos, end_pos_info = parts[0], parts[-1].strip('[]').split(',')
                        adjusted_start_pos = int(start_pos) + int(end_pos_info[0])
                        adjusted_end_pos = int(start_pos) + int(end_pos_info[0]) + int(end_pos_info[1]) - 1
                        header = f">{organism}_CRISPR{crispr_count}_{adjusted_start_pos}_{adjusted_end_pos}"
                        spacers.append(f"{header}\n{spacer_sequence}\n")  # 将spacer信息添加到列表中

    # 仅当找到spacer序列时才写入文件
    if spacers:
        with open(output_file_path, 'w') as output_file:
            for spacer in spacers:
                output_file.write(spacer)
        print(f"SPACER序列已以FASTA格式保存到 {output_file_path}")
    else:
        print("未找到SPACER序列，不创建文件。")

def main():
    parser = argparse.ArgumentParser(description='Extract CRISPR spacers to FASTA format.')
    parser.add_argument('-i', '--input', required=True, help='Input file path')
    parser.add_argument('-o', '--output', required=True, help='Output file path')

    args = parser.parse_args()

    extract_spacers_to_fasta(args.input, args.output)

if __name__ == "__main__":
    main()
