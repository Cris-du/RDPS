#!/usr/bin/env python3

import argparse
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord  # 确保导入 SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation

def parse_faa(faa_file):
    """
    解析faa文件，提取蛋白质信息。
    返回一个字典，键为病毒名称，值为蛋白质信息列表。
    """
    proteins = {}
    for record in SeqIO.parse(faa_file, "fasta"):
        # 提取蛋白质名称中的信息
        parts = record.description.split("#")
        virus_name = "_".join(record.id.split("_")[:-1])  # 去掉编号部分
        start = int(parts[1].strip())
        end = int(parts[2].strip())
        strand = -1 if parts[3].strip() == "-1" else 1
        protein_id = parts[0].split()[0]
        
        # 添加到字典
        if virus_name not in proteins:
            proteins[virus_name] = []
        proteins[virus_name].append({
            "protein_id": protein_id,
            "start": start,
            "end": end,
            "strand": strand,
            "translation": str(record.seq)
        })
    return proteins

def get_genome_lengths(fna_file):
    """
    读取.fna文件并返回每个基因组序列的长度。
    返回一个字典，键为序列ID，值为序列长度。
    """
    genome_lengths = {}
    for record in SeqIO.parse(fna_file, "fasta"):
        genome_lengths[record.id] = len(record.seq)
    return genome_lengths

def convert_to_gbk(fna_file, faa_file, output_file):
    """
    将fna和faa文件转换为gbk格式。
    只输出那些在faa文件中有对应蛋白质的病毒。
    """
    # 获取基因组序列长度
    genome_lengths = get_genome_lengths(fna_file)

    # 解析faa文件
    proteins = parse_faa(faa_file)

    # 打开输出文件
    with open(output_file, "w") as gbk_handle:
        # 解析fna文件
        for genome_record in SeqIO.parse(fna_file, "fasta"):
            virus_name = genome_record.id
            genome_seq = genome_record.seq
            genome_length = genome_lengths[virus_name]

            # 检查是否有对应的蛋白质信息
            if virus_name not in proteins or not proteins[virus_name]:
                continue  # 如果没有对应的蛋白质，跳过该病毒

            # 创建SeqRecord对象
            features = []
            for protein in proteins[virus_name]:
                # 验证蛋白质位置
                if protein["start"] < 1 or protein["end"] > genome_length:
                    raise ValueError(f"Protein position out of range: {protein['start']}..{protein['end']}")

                # 创建FeatureLocation
                if protein["strand"] == -1:
                    location = FeatureLocation(protein["start"] - 1, protein["end"], strand=-1)
                    cds_note = f"complement({protein['start']}..{protein['end']})"
                else:
                    location = FeatureLocation(protein["start"] - 1, protein["end"], strand=1)
                    cds_note = f"{protein['start']}..{protein['end']}"

                # 创建SeqFeature对象
                feature = SeqFeature(
                    location=location,
                    type="CDS",
                    qualifiers={
                        "protein_id": protein["protein_id"],
                        "translation": protein["translation"],
                        "note": cds_note
                    }
                )
                features.append(feature)

            # 创建新的SeqRecord对象，并添加必要的注释
            new_record = SeqRecord(
                seq=genome_seq,
                id=virus_name,
                name=virus_name,
                description=virus_name,  # 设置 DESCRIPTION 字段为病毒名称
                annotations={
                    "molecule_type": "DNA",  # 添加 molecule_type 注释
                    "topology": "linear",
                    "data_file_division": "UNK"
                }
            )
            new_record.features = features

            # 写入GBK格式
            SeqIO.write(new_record, gbk_handle, "genbank")
            gbk_handle.write("\n")  # 不同病毒之间用空行分隔

def main():
    parser = argparse.ArgumentParser(description="Convert fna and faa files to gbk format.")
    parser.add_argument("-fna", required=True, help="Input fna file (virus genome sequences).")
    parser.add_argument("-faa", required=True, help="Input faa file (protein sequences).")
    parser.add_argument("-o", required=True, help="Output gbk file.")
    args = parser.parse_args()

    convert_to_gbk(args.fna, args.faa, args.o)

if __name__ == "__main__":
    main()
