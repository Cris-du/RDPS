# Viral and Microbial Abundance caculation

---
## Install dependencies  
为了进行病毒丰度计算  
`bowtie2 v2.3.5.1`,相关配置方法可参照[bowtie2](https://github.com/BenLangmead/bowtie2)  
`bamm v1.7.3`,相关配置方法可参照[bamm](https://github.com/ecogenomics/BamM)  
`samtools v1.9`,相关配置方法可参照[samtools](https://github.com/samtools/samtools)  
`bedtools v2.31.1`,相关配置方法可参照[bedtools](https://plink.readthedocs.io/en/latest/bedtools_int/)  

为了进行原核微生物基因组丰度计算  
`CoverM v0.7.0`,相关配置方法可参照[coverm](https://github.com/wwood/CoverM)  

筛选覆盖长度比率＞0.7的contig名称  
`filter_coverage_result_seqname.py`  
筛选目标contig覆盖深度结果  
`filter_contig_depth.py`  
contig`bed`文件生成  
`bed_contigs.py`  
contig length.txt文件生成  
`contig_length.py`  
标准化丰度  
`normalized_contigs_depth.py``normalized_bin_depth.py`

你需要可以运行以下命令  
`bowtie2-build`  
`bowtie2`  
`samtools`  
`bamm`  
`bedtools`  
`coverm`  

对`GOHVGD`或`GOHMGD`进行索引构建  
```
bowtie2-build GOHVGD/GOHMGD_contigs_seq.fasta GOHVGD/GOHMGD_contigs_index
```

对测序文件进行viral contig/mag contig序列映射  
双端  
```
bowtie2 -p 64 -x GOHVGD/GOHMGD_contigs_index -1 SampleID_qced_forward.fq.gz -2 SampleID_qced_reverse.fq.gz -S GOHVGD/GOHMGD_map_SampleID.sam
```  
单端  
```
bowtie2 -p 64 -x GOHVGD/GOHMGD_contigs_index -U SampleID_qced_singled.fq.gz -S GOHVGD/GOHMGD_map_SampleID.sam
```
将`sam`文件转换成`bam`文件  
```
samtools view -@ 4 -bS GOHVGD/GOHMGD_map_SampleID.sam > GOHVGD/GOHMGD_map_SampleID.bam
```
对`bam`文件进行排序  
```
samtools sort -@ 4 -m 4G GOHVGD/GOHMGD_map_SampleID.bam -o GOHVGD/GOHMGD_map_sort_SampleID.bam
```

对`bam`文件的reads进行质量控制  
```
bamm filter -b GOHVGD/GOHMGD_map_sort_SampleID.bam --percentage_id 0.95 --percentage_aln 0.9 -o GOHVGD/GOHMGD_map_sort_filtered_SampleID.bam
```
`bam`二次排序并进行索引构建  
```
samtools sort -@ 4 -m 4G -o GOHVGD/GOHMGD_map_double_sort_filtered_SampleID.bam GOHVGD/GOHMGD_map_sort_filtered_SampleID.bam && samtools index GOHVGD/GOHMGD_map_double_sort_filtered_SampleID.bam
```
病毒丰度计算  
生成`bed`文件与`contig_length.txt`  
```
bed_contigs.py GOHVGD_contigs_seq.fasta GOHVGD_contigs_seq.bed
contig_length.py GOHVGD_contigs_seq.fasta GOHVGD_contigs_length.txt
```
contig覆盖长度比率计算  
```
bedtools coverage -a GOHVGD_contigs_seq.bed -sorted -g GOHVGD_contigs_length.txt -b GOHVGD_map_double_sort_filtered_SampleID.bam > GOHVGD_SampleID_coverage_length_rate.txt
```
contig平均覆盖深度计算  
```
bamm parse -b GOHVGD_map_double_sort_filtered_SampleID.bam -m tpmean -t 2 -c GOHVGD_SampleID_mean_depth.txt
```
筛选覆盖长度比率＞0.7的contig名称  
```
filter_coverage_result_seqname.py -i GOHVGD_SampleID_coverage_length_rate.txt -o GOHVGD_SampleID_coverage_length_rate_0.7_seqname.txt -c 0.7
```
筛选出覆盖长度比率＞0.7的contig平均覆盖深度结果  
```
filter_contig_depth.py -ic GOHVGD_SampleID_coverage_length_rate_0.7_seqname.txt -id GOHVGD_SampleID_mean_depth.txt -o GOHVGD_SampleID_mean_depth_clr_0.7.txt
```
标准化病毒contigs丰度  
```
normalized_contigs_depth.py -rc SampleID_reads_counts -id GOHVGD_SampleID_mean_depth_clr_0.7.txt -o normalized_GOHVGD_SampleID_mean_depth_clr_0.7.txt 
```
微生物bin丰度计算(将所有`bin.fa`文件移动至统一目录`GOHMGD_bin_dir`)  
```
coverm genome -d GOHMGD_bin_dir -b GOHMGD_map_double_sort_filtered_SampleID.bam -o GOHMGD_SampleID_coverm_meandepth.txt -m trimmed_mean -t 4
```
标准化MAG bin丰度  
```
normalized_bin_depth.py -rc SampleID_reads_counts -id GOHMGD_SampleID_coverm_meandepth.txt -o normalized_GOHMGD_SampleID_coverm_meandepth.txt
```
