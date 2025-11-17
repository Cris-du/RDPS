# Viral taxonomic assignment  
---
## Install dependencies  
### 为了蛋白质比对  
`diamond v2.1.8`,相关配置方法可参照[diamond](https://github.com/bbuchfink/diamond)  

### 为了根据BLASTp结果计算AAI  
`amino_acid_identity.py`,相关配置方法来源于[MGV](https://github.com/snayfach/MGV/blob/master/aai_cluster/README.md)  

### 为了过滤aai结果  
`filter_aai.py`,相关配置方法来源于[MGV](https://github.com/snayfach/MGV/blob/master/aai_cluster/README.md)  

### 为了MCL聚类  
`MCL v22-282`,相关配置方法可参照[MCL](https://github.com/micans/mcl)  

### 你需要可以运行以下命令  
`diamond`  
`mcl`  

## 自定义脚本  
### 为了计算病毒蛋白质数目  
`sum_virus_protein_counts.py`  

### 为了计算匹配蛋白质数目  
`caculate_ryseq_match_refseq_protein_counts.py`  

### 为了计算匹配蛋白质百分比  
`percent_match_protein_jisuan.py`  

### 为了提取最终识别结果  
`filter_count_match_precent.py`  

## 执行操作  
### GOHVGD属级与科级分配  
移动所有样本的vOTU代表性contig序列蛋白质`faa`文件`sample_id_vOTU_precontigs_protein.faa`至同一目录下,并进行合并至同一个faa文件,为`GOHVGD_vOTU_precontigs_protein.faa`  
```
cat *_protein.faa > GOHVGD_vOTU_precontigs_protein.faa
```

制作diamond比对数据库  
```
diamond makedb --in GOHVGD_vOTU_precontigs_protein.faa --db ./GOHVGD_vOTU_precontigs_protein --threads 64
```

对不同样本分别进行blastp比对，目的是为了加快处理速度以及降低内存资源消耗，为了确保全部的序列都能进入blastp报告结果，故设置max_target_seqs为一个极大值，用户可根据自己的数据库规模自行调整：
```
diamond blastp --query sample_id_vOTU_precontigs_protein.faa --db ./GOHVGD_vOTU_precontigs_protein --out sample_id_vOTU_precontigs_protein_blastp.txt --outfmt 6 --evalue 1e-5 --max-target-seqs 10000000
```

根据blastp结果计算每个样本的AAI  
```
python ./amino_acid_identity.py --in_faa sample_id_vOTU_precontigs_protein.faa --in_blast sample_id_vOTU_precontigs_protein_blastp.txt --out_tsv sample_id_vOTU_precontigs_protein_aai.txt
```

过滤边缘并准备MCL输入  
属级  
```
python ./filter_aai.py --in_aai sample_id_vOTU_precontigs_protein_aai.txt --min_percent_shared 20 --min_num_shared 0 --min_aai 50 --out_tsv sample_id_vOTU_precontigs_protein_genus_edges.txt
```
科级  
```
python ./filter_aai.py --in_aai sample_id_vOTU_precontigs_protein_aai.txt --min_percent_shared 10 --min_num_shared 0 --min_aai 20 --out_tsv sample_id_vOTU_precontigs_protein_family_edges.txt
```
对属级和科级的`edges.txt`分别进行合并为`GOHVGD_genus_edges.txt`和`GOHVGD_family_edges.txt`  
```
cat *.txt > GOHVGD_genus(family)_edges.txt
```

执行基于MCL的聚类  
```
mcl GOHVGD_genus_edges.txt -te 64 -I 2.0 --abc -o GOHVGD_genus_clusters.txt
```
```
mcl GOHVGD_family_edges.txt -te 64 -I 1.2 --abc -o GOHVGD_family_clusters.txt
```
在输出中，每一行都代表每个集群的成员（包括单例）

### 病毒分类学分配  
收集ICTV MSL39 v2分类学系统病毒在Refseq数据库中的蛋白质数据集`ictv_msl39v2_in_refseq_protein.faa`,进行diamond比对数据库构建  
```
diamond makedb --in ictv_msl39v2_in_refseq_protein.faa --db ./ictv_msl39v2_in_refseq_protein --threads 64
```
提取不同样本vOTU代表性contig序列的完整蛋白质序列,目的是为了加快处理速度以及降低内存资源消耗  
```
awk '/^>/{keep=0} /^>.*partial=/ && /^>.*partial=00/{keep=1} keep' sample_id_vOTU_precontigs_protein.faa > sample_id_vOTU_precontigs_complete_protein.faa
```

blastp比对  
```
diamond blastp --query sample_id_vOTU_precontigs_complete_protein.faa --db ./ictv_msl39v2_in_refseq_protein --out sample_id_vOTU_precontigs_complete_protein_blastp.txt --outfmt 6 --min-score 50 --max-target-seqs 10000000
```

计算vOTU代表性contig的完整蛋白质数目  
```
python ./sum_virus_protein_counts.py -i sample_id_vOTU_precontigs_complete_protein_protein.faa -o sample_id_vOTU_precontigs_complete_protein_counts.txt
```

计算vOTU代表性contig完整蛋白质匹配ICTV标准病毒蛋白质的数目  
```
python ./caculate_ryseq_match_refseq_protein_counts.py -i sample_id_vOTU_precontigs_complete_protein_blastp.txt -o sample_id_match_protein_counts.txt
```

计算匹配蛋白质百分比  
```
python ./percent_match_protein_jisuan.py -i1 sample_id_vOTU_precontigs_complete_protein_counts.txt -i2 sample_id_match_protein_counts.txt -o sample_id_match_protein_percent.txt
```

提取各样本vOTU代表性contig与ICTV标准病毒分配结果  
```
python ./filter_count_match_precent.py -i1 sample_id_vOTU_precontigs_complete_protein_counts.txt -i2 sample_id_match_protein_percent.txt -o sample_id_match_protein_percent_filiter50_count5_filter.txt
```
合并所有样本的vOTU代表性contig与ICTV标准病毒分配结果`GOHVGD_map_ICTV_msl39_v2.txt`  
对于一条GOHVGD vOTU代表性contig匹配多条ICTV标准病毒的情况,采取这些ICTV标准病毒未出现分类分歧的最低层级类别作为其分类,如:
| GOHVGD   | ICTV | Realm | Kingdom | Phylum | Class | Order |
|----------|------|--------|----------|---------|--------|--------|
| virus_A  | X1   | R1     | K1       | P1      | C1     | D1     |
| virus_A  | X2   | R1     | K1       | P1      | C2     | D3     |
| virus_A  | X3   | R1     | K1       | P2      | C3     | D4     |

此时virus_A匹配的多条ICTV标准病毒中，Kingdom层级为未出现分类分歧的最低层级，类别为K1,故virus_A的分类为Realm：R1、Kingdom：K1,其余层级未知,可参考脚本`merge_same_class_virus_taxa.py`
