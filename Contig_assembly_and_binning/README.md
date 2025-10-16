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
单端测序：`RUNID_single_reads.fq.gz`  
双端测序：`RUNID_forward_reads.fq.gz`, `RUNID_reverse_reads.fq.gz`  
单端命令：`fastp -i RUNID_single_reads.fq.gz -o RUNID_single_fastped_reads.fq.gz -h RUNID_single_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6`  
双端命令：`fastp -i RUNID_forward_reads.fq.gz -I RUNID_reverse_reads.fq.gz -o RUNID_forward_fastped_reads.fq.gz -O RUNID_reverse_fastped_reads.fq.gz -h RUNID_paired_fastped_reads_report.html -Q --thread=20 --length_required=15 --n_base_limit=5 --compression=6`  

合并相同样本的不同测序reads文件(`fastp`质控后)  
单端文件：`cat *single_fastped_reads.fq.gz > sampleID_merge_single_fastped_reads.fq.gz`  
双端文件：`cat *forward_fastped_reads.fq.gz > sampleID_merge_forward_fastped_reads.fq.gz, cat *reverse_fastped_reads.fq.gz > sampleID_merge_reverse_fastped_reads.fq.gz`  

使用`megahit`进行contig拼接  
单端测序文件拼接: `megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -r sampleID_merge_single_fastped_reads.fq.gz -o sampleID_raw_contigs.fa`  
双端测序文件拼接：`megahit --continue --min-count 2 --k-min 21 --k-max 255 --k-step 4 -t 20 -1 sampleID_merge_forward_fastped_reads.fq.gz -2 sampleID_merge_reverse_fastped_reads.fq.gz -o sampleID_raw_contigs.fa`  

过滤出长度≥1kb的contigs  
`seqkit seq -g -j 20 -m 1000 sampleID_raw_contigs.fa > sampleID_filter_1kb_contigs.fa`  

获得sam文件与bbmap_depth文件  
单端：`bbmap.sh in=sampleID_merge_single_fastped_reads.fq.gz ref=sampleID_filter_1kb_contigs.fa nodisk k=15 minid=0.9 keepnames=t covstats=sampleID_depth_bbmap.txt minaveragequality=5 outm=sampleID_bbmap.sam threads=64`  
双端：`bbmap.sh in=sampleID_merge_forward_fastped_reads.fq.gz in2=sampleID_merge_reverse_fastped_reads.fq.gz ref=sampleID_filter_1kb_contigs.fa nodisk k=15 minid=0.9 keepnames=t covstats=sampleID_depth_bbmap.txt minaveragequality=5 outm=sampleID_bbmap.sam threads=64`  
转换为bam文件,并进行排序与索引  
转换：`samtools view -bS -h -@ 4 sampleID_bbmap.sam -o sampleID_bbmap.bam`  
排序与索引：`samtools sort -@ 4 -o sampleID_sorted_bbmap.bam sampleID_bbmap.bam && samtools index sampleID_sorted_bbmap.bam` 
获得jgi_depth文件  
`jgi_summarize_bam_contig_depths --outputDepth sampleID_jgi_depth.txt sampleID_sorted_bbmap.bam`  
maxbin与metabat2分箱  
maxbin:`run_MaxBin.pl -contig sampleID_filter_1kb_contigs.fa -abund sampleID_depth_bbmap.txt -min_contig_length 1000 -thread 64 -out sampleID_maxbin_bins`  
metabat2:`metabat2 -i sampleID_filter_1kb_contigs.fa -a sampleID_jgi_depth.txt -m 1500 -v --cvExt -o sampleID_metabat2_bins -t 64`  
使用metawrap对maxbin与metabat2分箱结果进行精炼  
`metaWRAP bin_refinement -t 40 -c 50 -x 5 -o sampleID_metawrap_bins -A sampleID_maxbin_bins -B sampleID_metabat2_bins --keep-ambiguous`  
使用metawrap对仅在maxbin或metabat2成功分箱的sampleID的bin进行质控
`metaWRAP bin_refinement -t 40 -c 50 -x 5 -o sampleID_metabat2(maxbin)_bins_metawrap_checkm -A sampleID_metabat2(maxbin)_bins --keep-ambiguous`  
