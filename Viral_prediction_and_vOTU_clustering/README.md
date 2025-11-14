# 病毒预测与vOTU聚类
---
## Install dependencies  
### 为了过滤≥ 3kb contigs  
`seqkit v2.10.1`,相关配置方法可参照[seqkit](https://github.com/shenwei356/seqkit)  

### 为了virus初次预测  
`genomad v1.7.1`,相关配置方法可参照[genomad](https://github.com/apcamargo/genomad/tree/main)  

### 为了病毒基因组质量检测  
`checkv v1.0.1`,相关配置方法可参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)  

### 为了vOTU聚类  
`anicalc.py`, `aniclust.py`来源于`checkv`,相关配置参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)  

### 你需要可以运行以下命令  
`seqkit`  
`genomad`  
`checkv`  
`makeblastdb`  
`blastn`  

## 自定义脚本  
### provirus边界识别与确认  
`check_provirus.py`  

## 执行操作  
### 病毒识别  
过滤出长度≥3kb的contigs  
```
seqkit seq -g -j 20 -m 3000 ./sample_id_megahit/final.contigs.fa > sample_id_filter_3kb_contigs.fa
```

使用`genomad`进行病毒初次预测  
下载的病毒标记数据库`genomad_db`  
```
genomad download-database ./genomad_db
```  
病毒初次预测  
```
genomad end-to-end --cleanup -t 8 --splits 8 sample_id_filter_3kb_contigs.fa ./sample_id_step1_genomad ./genomad_db
```

使用`checkv`进行病毒质量检测  
```
checkv end_to_end ./sample_id_step1_genomad/sample_id_step1_genomad_summary/sample_id_step1_genomad_virus.fna ./sample_id_step1_genomad_step1_checkv -t 4
```

基于`./sample_id_step1_genomad_step1_checkv/quality_summary.tsv提取非provirus病毒、无需修剪的provirus以及经`checkv`修剪边界的provirus序列  
```
python ./check_provirus.py -it ./sample_id_step1_genomad_step1_checkv/quality_summary.tsv -ifc ./sample_id_step1_genomad_step1_checkv/proviruses.fna -ifg ./sample_id_step1_genomad_step1_checkv/viruses.fna -o sample_id_no_provirus_virus.fna -og sample_id_provirus_part1.fna -ogc sample_id_provirus_part2.fna
```
使用`genomad`对经`checkv`修剪边界的provirus序列进行二次病毒确认
```
genomad end-to-end --cleanup -t 8 --splits 8 sample_id_provirus_part2.fna ./sample_id_provirus_part2_step2_genomad ./genomad_db
```

使用`checkv`对重新确认为病毒的修剪边界provirus进行病毒质量检测  
```
checkv end_to_end ./sample_id_provirus_part2_step2_genomad/sample_id_provirus_part2_step2_genomad_summary/sample_id_provirus_part2_step2_genomad_virus.fna sample_id_step2_genomad_provirus_step2_checkv -t 4
```
合并`sample_id_no_provirus_virus.fna`,`sample_id_provirus_part1.fna`,`sample_id_provirus_part2_step2_genomad_virus.fna`记为`sample_id_virus_final.fna`,所有样本的病毒结果组成`GOHVGD`  

### vOTU聚类  
对`GOHVGD`进行vOTU聚类,参照[checkv](https://bitbucket.org/berkeleylab/checkv/src/master/#markdown-header-checkv-database)的Supporting code提供的方法流程,由Nayfach, S.等人提供：Nayfach, S., Camargo, A.P., Schulz, F. et al. CheckV assesses the quality and completeness of metagenome-assembled viral genomes. Nat Biotechnol 39, 578–585 (2021).[https://doi.org/10.1038/s41587-020-00774-7](https://doi.org/10.1038/s41587-020-00774-7)  

合并所有`sample_id_virus_final.fna`为`GOHVGD_all_viral_contigs.fna`
创建blast+ database  
```
makeblastdb -in GOHVGD_all_viral_contigs.fna -dbtype nucl -out ./GOHVGD_db
```
对不同sample_id分别进行blastn比对,目的是为了加快处理速度以及降低内存资源消耗,为了确保全部的序列都能进入blastn报告结果,故设置max_target_seqs为一个极大值,用户可根据自己的数据库规模自行调整  
```
blastn -query sample_id_virus_final.fna -db ./GOHVGD_db -outfmt '6 std qlen slen' -max_target_seqs 100000000 -o sample_id_blastn.txt -num_threads 64
```
calculate pairwise ANI by combining local alignments between sequence pairs  
```
anicalc.py -i sample_id_blastn.txt -o sample_id_ani.txt
```
将所有`sample_id_ani.tsv`移动至单一目录`GOHVGD_ani_dir`下,合并为`GOHVGD_ani.txt`  
```
(head -n 1 ./GOHVGD_ani_dir/*.txt | head -n 1 && tail -n +2 -q ./GOHVGD_ani_dir/*.txt) > merged.txt
```
Finally, perform CD-HIT-like clustering using the MIUVIG recommended-parameters (95% ANI + 85% AF):  
```
aniclust.py --fna GOHVGD_all_viral_contigs.fna --ani GOHVGD_ani.txt --out GOHVGD_vOTU_clusters.txt --min_ani 95 --min_tcov 85 --min_qcov 0
```
