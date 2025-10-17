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
`merge_ani_tsv.py`为本人自己写的脚本,仅供参考  

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
checkv end_to_end sampleID_step1_genomad_virus.fna sampleID_step1_genomad_step1_checkv -t 4
```

基于`./sampleID_step1_genomad_step1_checkv/quality_summary.tsv识别provirus边界    
```
python ./check_provirus.py -it ./sampleID_step1_genomad_step1_checkv/quality_summary.tsv -ifc ./sampleID_step1_genomad_step1_checkv/proviruses.fna -ifg sampleID_step1_genomad_virus.fna -o sampleID_no_provirus_virus.fna -og sampleID_provirus_part1.fna -ogc sampleID_provirus_part2.fna
```
使用`genomad`对`sampleID_provirus_part2.fna`进行二次病毒确认
```
genomad end-to-end --cleanup -t 8 --splits 8 sampleID_provirus_part2.fna sampleID_provirus_part2_step2_genomad ./genomad_db
```

使用`checkv`对`./sampleID_provirus_part2_step2_genomad/sampleID_provirus_part2_step2_genomad_summary/sampleID_provirus_part2_step2_genomad_virus.fna`进行病毒质量检测  
```
checkv end_to_end ./sampleID_provirus_part2_step2_genomad_virus.fna sampleID_step2_genomad_provirus_step2_checkv -t 4
```
合并`sampleID_no_provirus_virus.fna`,`sampleID_provirus_part1.fna`,`sampleID_provirus_part2_step2_genomad_virus.fna`记为`sampleID_virus_final.fna`,所有样本的病毒结果组成`GOHVGD`  

对`GOHVGD`进行vOTU聚类,参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)的Supporting code提供的方法流程,由Nayfach, S.等人提供：Nayfach, S., Camargo, A.P., Schulz, F. et al. CheckV assesses the quality and completeness of metagenome-assembled viral genomes. Nat Biotechnol 39, 578–585 (2021). [https://doi.org/10.1038/s41587-020-00774-7](https://doi.org/10.1038/s41587-020-00774-7)  

### Rapid genome clustering based on pairwise ANI  
合并所有`sampleID_virus_final.fna`为`GOHVGD.fna`
First, create a blast+ database:  
```
makeblastdb -in GOHVGD.fna -dbtype nucl -out GOHVGD_db
```
Next, 对不同sampleID分别进行blastn比对,目的是为了加快处理速度以及降低内存资源消耗,为了确保全部的序列都能进入blastn报告结果,故设置max_target_seqs为一个极大值,用户可根据自己的数据库规模自行调整:  
```
blastn -query sampleID_virus_final.fna -db GOHVGD_db -outfmt '6 std qlen slen' -max_target_seqs 100000000 -o sampleID_blastn.tsv -num_threads 64
```
Next, calculate pairwise ANI by combining local alignments between sequence pairs:  
```
anicalc.py -i sampleID_blastn.tsv -o sampleID_ani.tsv
```
将所有`sampleID_ani.tsv`移动至单一目录GOHVGD_ani_dir下,合并为`GOHVGD_ani.tsv`  
```
python merge_ani_tsv.py -i GOHVGD_ani_dir -o GOHVGD_ani.tsv
```
Finally, perform CD-HIT-like clustering using the MIUVIG recommended-parameters (95% ANI + 85% AF):  
```
aniclust.py --fna GOHVGD.fna --ani GOHVGD_ani.tsv --out GOHVGD_clusters.tsv --min_ani 95 --min_tcov 85 --min_qcov 0
```
