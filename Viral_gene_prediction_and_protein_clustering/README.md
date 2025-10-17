# Viral gene prediction and protein clustering
---
## Install dependencies  
为了蛋白质预测  
`Prodigal V2.11.0-gv`,相关配置方法可参照[prodigal-gv](https://github.com/apcamargo/prodigal-gv)  

为了蛋白质聚类成蛋白质簇  
`CD-HIT v4.8.1`,相关配置方法可参照[cdhit](https://github.com/weizhongli/cdhit)  

为了识别蛋白质簇的代表性蛋白  
`transformat_pcs_report.py`    

你需要可以运行以下命令  
`prodigal-gv`  
`cd-hit`  

使用`fastp`进行reads质控（包括修剪, 去除接头）  
准备已经下载好的宏基因组测序reads文件  
单端测序：`RUNID_single_reads.fq.gz`  
双端测序：`RUNID_forward_reads.fq.gz`, `RUNID_reverse_reads.fq.gz`  

单端命令  
```
fastp -i RUNID_single_reads.fq.gz -o RUNID_single_fastped_reads.fq.gz -h RUNID_single_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6
```
双端命令  
```
fastp -i RUNID_forward_reads.fq.gz -I RUNID_reverse_reads.fq.gz -o RUNID_forward_fastped_reads.fq.gz -O RUNID_reverse_fastped_reads.fq.gz -h RUNID_paired_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6
```

合并相同样本的不同测序reads文件(`fastp`质控后)  
单端文件
```
cat *single_fastped_reads.fq.gz > sampleID_merge_single_fastped_reads.fq.gz
```
双端文件
```
cat *forward_fastped_reads.fq.gz > sampleID_merge_forward_fastped_reads.fq.gz, cat *reverse_fastped_reads.fq.gz > sampleID_merge_reverse_fastped_reads.fq.gz
```

使用`megahit`进行contig拼接  
单端测序文件拼接
```
megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -r sampleID_merge_single_fastped_reads.fq.gz -o sampleID_raw_contigs.fa
```
双端测序文件拼接
```
megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -1 sampleID_merge_forward_fastped_reads.fq.gz -2 sampleID_merge_reverse_fastped_reads.fq.gz -o sampleID_raw_contigs.fa
```
