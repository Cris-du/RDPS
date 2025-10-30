# 系统发育分析
---
## Install dependencies  
为了进行蛋白质去冗余  
`cdhit v4.8.1`,相关配置方法可参照[cdhit](https://github.com/weizhongli/cdhit)  

为了进行Caudoviricetes标志蛋白识别  
`diamond v2.1.8`,相关配置方法可参照[diamond](https://github.com/bbuchfink/diamond?tab=readme-ov-file)  

为了进行Caudoviricetes标志蛋白聚类  
`MMseqs2 v13.4.5`,相关配置方法可参照[mmseqs2](https://github.com/soedinglab/MMseqs2)  

为了进行多序列比对  
`MUSCLE v5.2`,相关配置方法可参照[muscle](https://github.com/rcedgar/muscle)  

为了进行多序列比对结果过滤  
`trimAl v1.5`,相关配置方法可参照[trimAl](https://vicfero.github.io/trimal/)  

为了构建系统发育树  
`FastTree v2.1.11`,相关配置方法可参照[fasttree](https://software.cqls.oregonstate.edu/updates/fasttree-2.1.11/)  

为了筛选GOHVGD中完整性≥50%的contigs的完整蛋白质  
`filter_GOHVGD_50_compless_protein.py`  

你需要可以运行以下命令  
`cdhit`  
`mmseqs`  
`muscle-linux-x86.v5.2`  
`trimal`  
`FastTree`  

对NCBI RefSeq (release 225)的经典Caudoviricetes病毒标志蛋白序列`Terl\MCP\Portal`进行去冗余  
```
cd-hit -i NCBI_refseq_terl(mcp/portal).faa -o drep_NCBI_refseq_terl(mcp/portal).faa -c 1.0 -aL 1.0 -aS 1.0 -n 5 -d 0 -T 16
```

筛选GOHVGD中完整性≥50%的contigs的完整蛋白质`GOHVGD_wanzheng_protein.faa`  
```
filter_GOHVGD_50_compless_protein.py -i GOHVGD_wanzheng_protein.faa -o GOHVGD_contigs_50_completess_wanzheng_protein.faa
```  

鉴定GOHVGD中的高质量Caudoviricetes病毒标志蛋白`Terl\MCP\Portal`序列数据集  
```
diamond makedb --in drep_NCBI_refseq_terl(mcp/portal).faa --db drep_NCBI_refseq_terl(mcp/portal)_db --threads 4
```
```
diamond blastp --query GOHVGD_contigs_50_completess_wanzheng_protein.faa --db drep_NCBI_refseq_terl(mcp/portal).faa --out GOHVGD_contigs_50_completess_wanzheng_protein_terl(mcp/portal)_blastpout.txt --al GOHVGD_contigs_50_completess_wanzheng_terl(mcp/portal).faa --outfmt 6 --evalue 1e-5 --max-target-seqs 5000000 --threads 2
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
