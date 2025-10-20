# Virus–Host infective relationship prediction  
---
## Install dependencies  
为了识别CRIPSR-SPACER序列  
`CRT-mod version 2.0rev1`,内置CRISPR-spacer识别工具为[CRT](https://www.room220.com/crt/)，相关配置方法可参照[CRT-mod](https://github.com/caseyh/crt-mod?tab=readme-ov-file)  

为了进行BLASTn  
`BLAST 2.12.0+`,相关配置方法来源于[MGV](https://github.com/snayfach/MGV/blob/master/aai_cluster/README.md)  

为了过滤aai结果  
[`filter_aai.py`](https://github.com/snayfach/MGV/blob/master/aai_cluster/filter_aai.py)  

为了识别完整蛋白质  
`filter_complete_protein.py`  

为了计算病毒蛋白质数目  
`sum_virus_protein_counts.py`  

为了计算匹配蛋白质数目  
`caculate_ryseq_match_refseq_protein_counts.py`  

为了计算匹配蛋白质百分比  
`percent_match_protein_jisuan.py`  

为了提取最终识别结果  
`filiter_percent_match.py`  
`filiter_count_protein.py`  

为了MCL聚类  
`MCL v22-282`,相关配置方法可参照[MCL](https://github.com/micans/mcl)  

你需要可以运行以下命令  
`diamond`  
`mcl`  

移动所有样本的vOTU代表性序列蛋白质`faa`文件`sampleID_vOTU_precontig_protein.faa`至同一目录下,并进行合并至同一个faa文件,为`GOHVGD_vOTU_precontig_protein.faa`  
```
cat *.faa > GOHVGD_vOTU_precontig_protein.faa
```

制作DIAMOND数据库  
```
diamond makedb --in GOHVGD_vOTU_precontig_protein.faa --db GOHVGD_vOTU_precontig_protein --threads 64
```

接下来，对不同sampleID分别进行blastp比对，目的是为了加快处理速度以及降低内存资源消耗，为了确保全部的序列都能进入blastp报告结果，故设置max_target_seqs为一个极大值，用户可根据自己的数据库规模自行调整：
```
diamond blastp --query sampleID_vOTU_precontig_protein.faa --db GOHVGD_vOTU_precontig_protein --out sampleID_vOTU_precontig_protein_blastp.tsv --outfmt 6 --evalue 1e-5 --max-target-seqs 10000000
```

根据blastp结果计算每个样本的AAI  
```
python amino_acid_identity.py --in_faa sampleID_vOTU_precontig_protein.faa --in_blast sampleID_vOTU_precontig_protein_blastp.tsv --out_tsv sampleID_vOTU_precontig_protein_aai.tsv
```

过滤边缘并准备 MCL 输入
```
python filter_aai.py --in_aai sampleID_vOTU_precontig_protein_aai.tsv --min_percent_shared 20 --min_num_shared 0 --min_aai 50 --out_tsv sampleID_vOTU_precontig_protein_genus_edges.tsv
```
```
python filter_aai.py --in_aai sampleID_vOTU_precontig_protein_aai.tsv --min_percent_shared 10 --min_num_shared 0 --min_aai 20 --out_tsv sampleID_vOTU_precontig_protein_family_edges.tsv
```
对genus和family水平的edges.tsv结果分别进行合并为`GOHVGD_genus_edges.tsv`和`GOHVGD_family_edges.tsv`  
```
cat *.tsv > GOHVGD_genus_edges.tsv/GOHVGD_family_edges.tsv
```

执行基于 MCL 的聚类  
```
mcl GOHVGD_genus_edges.tsv -te 64 -I 2.0 --abc -o GOHVGD_genus_clusters.txt
```
```
mcl GOHVGD_family_edges.tsv -te 64 -I 1.2 --abc -o GOHVGD_family_clusters.txt
```
在输出中，每一行都指示属于每个集群的成员（包括单例）

病毒分类
收集ICTV MSL39 v2的病毒在Refseq数据库中的蛋白质数据集`ictv_msl39v2_in_refseq_protein.faa`,进行DIAMOND比对数据库构建  
```
diamond makedb --in ictv_msl39v2_in_refseq_protein.faa --db ictv_msl39v2_in_refseq_protein --threads 64
```
提取识别GOHVGD vOTU标志性病毒contig的完整蛋白质  
```
python filter_complete_protein.py -i sampleID_vOTU_precontig_protein.faa -o sampleID_vOTU_precontig_complete_protein.faa
```

blastp比对  
```
diamond blastp --query sampleID_vOTU_precontig_complete_protein.faa --db ictv_msl39v2_in_refseq_protein --out sampleID_vOTU_precontig_complete_protein_blastp.tsv --outfmt 6 --min-score 50 --max-target-seqs 10000000
```

计算病毒蛋白质数目  
```
python sum_virus_protein_counts.py -i sampleID_vOTU_precontig_complete_protein.faa -o sampleID_vOTU_precontig_complete_protein_counts.tsv
```

计算匹配蛋白质数目  
```
python caculate_ryseq_match_refseq_protein_counts.py -i sampleID_vOTU_precontig_complete_protein_blastp.tsv -o sampleID_match_protein_counts.tsv
```

计算匹配蛋白质百分比  
```
python percent_match_protein_jisuan.py -i1 sampleID_vOTU_precontig_complete_protein_counts.tsv -i2 sampleID_match_protein_counts.tsv -o sampleID_match_protein_percent.tsv
```

为了提取最终识别结果  
step1  
```
python filiter_percent_match.py -i sampleID_match_protein_percent.tsv -o sampleID_match_protein_percent_filiter50.tsv
```
```
python filiter_count_protein.py -i1 sampleID_vOTU_precontig_complete_protein_counts.tsv -i2 sampleID_match_protein_percent_filiter50.tsv -o sampleID_match_protein_percent_filiter50_count5_filter.tsv
```
