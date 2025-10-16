# contig拼接与binning
---
<b>  Install dependencies </b>  
`fastp 0.23.3`  
`MEGAHIT v1.2.9`  
`samtools 1.19.2`  
`BBMap 38.18`  
`MetaBAT2 2.15`  
`MaxBin 2.2.7`  
`metaWRAP v=1.3.2`  
`seqkit v2.10.1`  
你需要可以运行以下命令  
`fastp`  
`megahit`  
`bbmap.sh`  
`samtools`  
`run_MaxBin.pl`  
`jgi_summarize_bam_contig_depths`  
`metabat2`  
`metaWRAP`  
`seqkit`  
使用`fastp`进行reads质控（包括修剪, 去除接头）  
准备已经下载好的宏基因组测序reads文件  
单端测序：`ID_single_reads.fq.gz`  
双端测序：`ID_forward_reads.fq.gz`, `ID_reverse_reads.fq.gz`  
单端命令：`fastp -i ID_single_reads.fq.gz -o ID_single_fastped_reads.fq.gz -h ID_single_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6`  
双端命令：`fastp -i ID_forward_reads.fq.gz -I ID_reverse_reads.fq.gz -o ID_forward_fastped_reads.fq.gz -O ID_reverse_fastped_reads.fq.gz -h ID_paired_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6`  

合并相同样本的不同测序reads文件(`fastp`质控后)
单端文件：cat *single_fastped_reads.fq.gz > sampleID_merge_single_fastped_reads.fq.gz  
双端文件：cat *forward_fastped_reads.fq.gz > sampleID_merge_forward_fastped_reads.fq.gz, cat *reverse_fastped_reads.fq.gz > sampleID_merge_reverse_fastped_reads.fq.gz

使用`megahit`进行contig拼接  
单端测序文件拼接: `megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -r sampleID_merge_single_fastped_reads.fq.gz -o raw_contigs.fa`  
双端测序文件拼接：`megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -1 sampleID_merge_forward_fastped_reads.fq.gz -2 sampleID_merge_reverse_fastped_reads.fq.gz -o raw_contigs.fa`  

过滤出长度≥1kb的contigs
`seqkit seq -g -j 20 -m 1000 raw_contigs.fa > filter_1kb_contigs.fa`  

