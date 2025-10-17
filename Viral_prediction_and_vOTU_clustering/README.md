# 病毒预测与vOTU聚类
---
## Install dependencies  
为了过滤≥ 3kb contigs  
`seqkit v2.10.1`,相关配置方法可参照[seqkit](https://github.com/shenwei356/seqkit)  

为了virus初次预测  
`genomad v1.7.1`,相关配置方法可参照[genomad](https://github.com/apcamargo/genomad/tree/main)  

为了病毒基因组质量检测  
`checkv v1.0.1`,相关配置方法可参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)  

provirus边界识别与确认  
`check_provirus.py`  

为了vOTU聚类  
`anicalc.py`, `aniclust.py`来源于`checkv`,相关配置参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)  

你需要可以运行以下命令  
`seqkit`  
`genomad`  
`checkv`  
`makeblastdb`  
`blastn`  

过滤出长度≥3kb的contigs  
```
seqkit seq -g -j 20 -m 3000 sampleID_raw_contigs.fa > sampleID_filter_3kb_contigs.fa
```

使用`genomad`进行病毒初次预测  
准备已经下载好的病毒分类标记数据库`./genomad_db`  
```
genomad download-database ./genomad_db
```  

对≥ 3kb contigs`sampleID_filter_3kb_contigs.fa`进行病毒初次预测  
```
genomad end-to-end --cleanup -t 8 --splits 8 sampleID_filter_3kb_contigs.fa sampleID_step1_genomad ./genomad_db
```
病毒识别结果文件位于`./sampleID_step1_genomad/sampleID_step1_genomad_summary/sampleID_step1_genomad_virus.fna`  

使用`checkv`进行病毒质量检测  
```
checkv end_to_end sampleID_genomad_step1_raw_virus_virus.fna sampleID_genomad_step1_raw_virus_virus -t 4
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
