# contig拼接与binning
---
## Install dependencies  
为了reads质控  
`fastp 0.23.3`,相关配置方法可参照[fastp](https://github.com/OpenGene/fastp)  

为了拼接contigs与过滤≥ 1kb contigs  
`MEGAHIT v1.2.9`,相关配置方法可参照[megahit](https://github.com/voutcn/megahit)  
`seqkit v2.10.1`,相关配置方法可参照[seqkit](https://github.com/shenwei356/seqkit)  

为了binning  
`samtools 1.19.2`,相关配置方法可参照[samtools](https://github.com/samtools/samtools)  
`BBMap 38.18`,相关配置方法可参照[bbmap](https://github.com/BioInfoTools/BBMap?tab=readme-ov-file)  
`MetaBAT2 2.15`,相关配置方法可参照[metabat2](https://bitbucket.org/berkeleylab/metabat/src/master/)  
`MaxBin 2.2.7`,相关配置方法可参照[maxbin](https://sourceforge.net/projects/maxbin/)  
`metaWRAP v=1.3.2`,相关配置方法可参照[metawrap](https://github.com/bxlab/metaWRAP)  

为了微生物基因组分类  
`GTDB-Tk v2.4.0`,相关配置方法可参照[GTDBTk](https://github.com/Ecogenomics/GTDBTk)  

你需要可以运行以下命令  
`fastp`  
`megahit`  
`seqkit`  
`samtools`  
`bbmap.sh`  
`jgi_summarize_bam_contig_depths`  
`run_MaxBin.pl`  
`metabat2`  
`metaWRAP`  
`gtdbtk`  

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


过滤出长度≥1kb的contigs  
```
seqkit seq -g -j 20 -m 1000 sampleID_raw_contigs.fa > sampleID_filter_1kb_contigs.fa
```
获得sam文件与bbmap_depth文件  
单端
```
bbmap.sh in=sampleID_merge_single_fastped_reads.fq.gz ref=sampleID_filter_1kb_contigs.fa nodisk k=15 minid=0.9 keepnames=t covstats=sampleID_depth_bbmap.txt minaveragequality=5 outm=sampleID_bbmap.sam threads=64
```
双端
```
bbmap.sh in=sampleID_merge_forward_fastped_reads.fq.gz in2=sampleID_merge_reverse_fastped_reads.fq.gz ref=sampleID_filter_1kb_contigs.fa nodisk k=15 minid=0.9 keepnames=t covstats=sampleID_depth_bbmap.txt minaveragequality=5 outm=sampleID_bbmap.sam threads=64
```

转换为bam文件,并进行排序与索引  
转换
```
samtools view -bS -h -@ 4 sampleID_bbmap.sam -o sampleID_bbmap.bam
```
排序与索引
```
samtools sort -@ 4 -o sampleID_sorted_bbmap.bam sampleID_bbmap.bam && samtools index sampleID_sorted_bbmap.bam
```
获得jgi_depth文件  
```
jgi_summarize_bam_contig_depths --outputDepth sampleID_jgi_depth.txt sampleID_sorted_bbmap.bam
```
maxbin与metabat2分箱  
maxbin
```
run_MaxBin.pl -contig sampleID_filter_1kb_contigs.fa -abund sampleID_depth_bbmap.txt -min_contig_length 1000 -thread 64 -out ./sampleID_maxbin_bins
```
metabat2
```
metabat2 -i sampleID_filter_1kb_contigs.fa -a sampleID_jgi_depth.txt -m 1500 -v --cvExt -o ./sampleID_metabat2_bins -t 64
```

使用metawrap对maxbin与metabat2分箱结果进行精炼  
```
metaWRAP bin_refinement -t 40 -c 50 -x 5 -o ./sampleID_metawrap_bins -A ./sampleID_maxbin_bins -B ./sampleID_metabat2_bins --keep-ambiguous
```

得到的metawrap精炼bin位于`./sampleID_metawrap_bins/metawrap_50_5_bins`  

使用metawrap对仅在maxbin或metabat2成功分箱的sampleID的bin进行质控  
```
metaWRAP bin_refinement -t 40 -c 50 -x 5 -o ./sampleID_metabat2(maxbin)_bins_metawrap -A ./sampleID_metabat2(maxbin)_bins --keep-ambiguous
```

人工筛选`.stats`中完整度≥50%且污染度≤5%的`bins`,作为通过`metawrap`质控的结果的`sampleID_metabat2(maxbin)_bins`,记为`sampleID_metabat2(maxbin)_bins_checked`  

合并`./sampleID_metabat2(maxbin)_bins_checked`以及`./sampleID_metawrap_bins/metawrap_50_5_bins`的`*bin.fa`，作为GOHMGD  

微生物MAG分类   
安装gtdb-tk数据库  
```
gtdbtk download-data --data-dir ./gtdbtk_db --batch 4
```

存放GOHMGD的`*bin.fa`于同一目录内，如`./GOHMGD/*bin.fa`  
gtdbtk分类命令
```
gtdbtk classify_wf --genome_dir ./GOHMGD --out_dir ./GOHMGD_gtdbtk_skip --data_dir ./gtdbtk_db --skip_ani_screen -x fa --cpus 10 --pplacer_cpus 10
```
