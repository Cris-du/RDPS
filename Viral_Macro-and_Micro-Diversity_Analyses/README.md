# Viral Macro-and Micro-Diversity Analyses
---
## Install dependencies  
为了进行病毒丰度计算  
`bowtie2 v2.3.5.1`,相关配置方法可参照[bowtie2](https://github.com/BenLangmead/bowtie2)  
`bamm v1.7.3`,相关配置方法可参照[bamm](https://github.com/ecogenomics/BamM)  
`samtools v1.9`,相关配置方法可参照[samtools](https://github.com/samtools/samtools)  
`bedtools v2.31.1`,相关配置方法可参照[bedtools](https://plink.readthedocs.io/en/latest/bedtools_int/)  

为了进行原核微生物基因组丰度计算  
`CoverM v0.7.0`,相关配置方法可参照[coverm](https://github.com/wwood/CoverM)  

为了进行微观多样性分析  
`metapop v13.4.5`,相关配置方法可参照[metapop](https://github.com/metaGmetapop/metapop)  

为了筛选覆盖率的病毒丰度结果  
`filter_cover_length.py`  

你需要可以运行以下命令  
`bowtie2-build`  
`bowtie2`  
`samtools`  
`bamm`  
`bedtools`  
`coverm`  
`metapop`  


对NCBI RefSeq (release 225)的经典Caudoviricetes病毒标志蛋白序列`Terl\MCP\Portal`进行去冗余  
```
cd-hit -i NCBI_refseq_terl(mcp/portal).faa -o drep_NCBI_refseq_terl(mcp/portal).faa -c 1.0 -aL 1.0 -aS 1.0 -n 5 -d 0 -T 16
```

筛选GOHVGD/GOV2.0中完整性≥50%的contigs的完整蛋白质`GOHVGD_wanzheng_protein.faa`  
```
filter_50_compless_protein.py -i GOHVGD/GOV2.0_wanzheng_protein.faa -o GOHVGD/GOV2.0_contigs_50_completess_wanzheng_protein.faa
```  

鉴定GOHVGD/GOV2.0中的高质量Caudoviricetes病毒标志蛋白`Terl\MCP\Portal`序列数据集  
```
diamond makedb --in drep_NCBI_refseq_terl(mcp/portal).faa --db drep_NCBI_refseq_terl(mcp/portal)_db --threads 4
```
```
diamond blastp --query GOHVGD/GOV2.0_contigs_50_completess_wanzheng_protein.faa --db drep_NCBI_refseq_terl(mcp/portal).faa --out GOHVGD/GOV2.0_contigs_50_completess_wanzheng_protein_terl(mcp/portal)_blastpout.txt --al GOHVGD/GOV2.0_contigs_50_completess_wanzheng_terl(mcp/portal).faa --outfmt 6 --evalue 1e-5 --max-target-seqs 5000000 --threads 2
```

对GOHVGD/GOV2.0以及Refseq的Caudoviricetes病毒标志蛋白`Terl\MCP\Portal`序列进行目级别聚类  
```
mmseqs easy-cluster terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq.faa terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_out terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_tmp --min-seq-id 0.269 -c 0.5 --cov-mode 1 --threads 40
```

对GOHVGD/GOV2.0/Refseq的`Terl\MCP\Portal`目级别代表序列进行系统发育树构建  
```
muscle-linux-x86.v5.2 -super5 terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster.faa -output terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster.afa -threads 10
```
```
trimal -in terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster.afa -out terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_trimal.fasta -htmlout terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_trimal.html -gappyout
```
```
FastTree -lg terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_trimal.fasta > terl(mcp/portal)_merge_GOHVGD_GOV2.0_Refseq_cluster_trimal_super5_lg_model.nwk
```
适用iTOL进行系统发育树可视化  
还缺少MAG的系统发育分析
