# 病毒蛋白功能多样性注释以及Auxiliary Metabolic Gene (AMG) Analysis

---
## Install dependencies  
为了进行病毒的蛋白功能多样性注释与辅助代谢基因（AMG）预测  
`dram-bio v1.5.0`,相关配置方法可参照[DRAM](https://github.com/WrightonLabCSU/DRAM)  
`virsorter v2.2.3`,相关配置方法可参照[Virsorter2](https://github.com/jiarong/VirSorter2)  

为了召回GOHVGD的原始蛋白质数据集  
`diamond v2.1.8`,相关配置方法可参照[diamond](https://github.com/bbuchfink/diamond)  
`tiqu_raw_protein_map_seqnam.py`  

你需要可以运行以下命令  
`virsorter2.sif`  
`DRAM-v.py`  
`diamond`  

由于DRAM-v只能接受virsorter2的输出结果，故需要对原始GOHVGD数据集进行virsorter2病毒重新预测  
```
virsorter2.sif run --seqname-suffix-off --viral-gene-enrich-off --provirus-off --prep-for-dramv  --rm-tmpdir --min-score 0 -i GOHVGD_pre_contig.fna -w GOHVGD_pre_contig_virsorter2_out -j 4 --min-length 0
```
DRAM-v进行病毒蛋白质注释  
```
DRAM-v.py annotate -i ./GOHVGD_pre_contig_virsoter2_out/for-dramv/final-viral-combined-for-dramv.fa -v ./GOHVGD_pre_contig_virsoter2_out/for-dramv/viral-affi-contigs-for-dramv.tab -o ./GOHVGD_pre_contig_virsoter2_dramv_annot --skip_trnascan --threads 40 --min_contig_size 0
```
DRAM-v进行AMG提取  
```
DRAM-v.py distill -i ./GOHVGD_virsoter2_dramv_annot/annotations.tsv -o ./GOHVGD_virsoter2_dramv_annot/GOHVGD_virsoter2_dramv_distill
```
手动筛选AMG结果，具体筛选标准为：保留代谢标记包含"M"且得分为1的基因。然而，由于某些功能类别的基因（如Peptidase，DNA methyltransferase，nucleotide）有可能是病毒自身生命活动所需的基因。这类基因通常不被认为是真正的辅助代谢基因，因此我们排除了包含“Peptidase”、“DNA methyltransferase”以及“nucleotide”相关关键词的基因。结果保存于`GOHVGD_raw_amg.tsv`  

召回GOHVGD的原始蛋白质数据集  
构建diamond blastp参考数据库  
```
diamond makedb --in ./GOHVGD_virsoter2_dramv_annot/genes.faa --db GOHVGD_dramv_protein_db --threads 4
```
进行diamond blastp召回比对  
```
diamond blastp --query GOHVGD_raw_protein.faa --db GOHVGD_dramv_protein_db --out GOHVGD_raw_protein_map_dramv_out_blastp.txt --outfmt 6 --id 100 --query-cover 100 --subject-cover 100 --evalue 1e-3 --max-target-seqs 5000000 --threads 2
```
进行相同病毒蛋白质名称对应结果提取  
```
tiqu_raw_protein_map_seqnam.py -i GOHVGD_raw_protein_map_dramv_out_blastp.txt -o GOHVGD_raw_protein_map_dramv_protein_seqname_map.txt
```
根据`GOHVGD_raw_protein_map_dramv_protein_seqname_map.txt`对`./GOHVGD_virsoter2_dramv_annot/annotations.tsv`与`GOHVGD_raw_amg.tsv`进行GOHVGD结果召回，获得最终GOHVGD的蛋白质功能注释结果以及AMG注释结果。  
