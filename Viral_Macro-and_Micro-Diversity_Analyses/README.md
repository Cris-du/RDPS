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

对`GOHVGD`进行索引构建  
```
bowtie2-build GOHVGD_contigs_seq.fasta GOHVGD_contigs_index
```

对测序文件进行contig序列映射  
双端  
```
bowtie2 -p 64 -x GOHVGD_contigs_index -1 SampleID_qced_forward.fq.gz -2 SampleID_qced_reverse.fq.gz -S GOHVGD_map_SampleID.sam
```  
单端  
```
bowtie2 -p 64 -x GOHVGD_contigs_index -U SampleID_qced_singled.fq.gz -S GOHVGD_map_SampleID.sam
```
将`sam`文件转换成`bam`文件  
```
samtools view -@ 4 -bS GOHVGD_map_SampleID.sam > GOHVGD_map_SampleID.bam
```
对`bam`文件进行排序  
```
samtools sort -@ 4 -m 4G GOHVGD_map_SampleID.bam -o GOHVGD_map_sort_SampleID.bam
```

对`bam`文件的reads进行质量控制  
```
bamm filter -b GOHVGD_map_sort_SampleID.bam --percentage_id 0.95 --percentage_aln 0.9 -o GOHVGD_map_sort_filtered_SampleID.bam
```
`bam`二次排序并进行索引构建  
```
samtools sort -@ 4 -m 4G -o GOHVGD_map_double_sort_filtered_SampleID.bam GOHVGD_map_sort_filtered_SampleID.bam && samtools index GOHVGD_map_double_sort_filtered_SampleID.bam
```

