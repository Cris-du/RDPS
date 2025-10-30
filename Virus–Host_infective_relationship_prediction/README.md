# Virus–Host infective relationship prediction  
---
## Install dependencies  
为了识别CRIPSR-SPACER序列  
`CRT-mod version 2.0rev1`,内置CRISPR-spacer识别工具为[CRT](https://www.room220.com/crt/),相关配置方法可参照[CRT-mod](https://github.com/caseyh/crt-mod?tab=readme-ov-file)  

为了进行BLASTn,也可通过checkv一起安装    
`BLAST 2.12.0+`,相关配置方法来源于[blast+](https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.12.0/)  

辅助脚本  
`filter_short_blastn_result.py`  
`filter_long_blastn_result.py`  
`merge_short_long_blastn_result.py`  
`derep_merge_result.py`  

你需要可以运行以下命令  
`blastn`  

根据GOHMGD的MAG序列`ID_bin.fa`识别CRIPSR-SPACER序列  
```
python crt-mod.py -i ID_bin.fa fasta -o ID_bin_CRISPRs_raw_report.txt --threads=1
```

提取并标准化CRIPSR-SPACER序列结果  
```
python standard_CRISPRs_raw_report.py -i ID_bin_CRISPRs_raw_report.txt -o ID_standard_CRISPRs.fasta
```
构建GOHVGD的blastn比对db
```
makeblastdb -in GOHVGD_nuc_seq.fa -dbtype nucl -out GOHVGD_nuc_seq_db
```

CRIPSR-SPACER序列与virus contigs进行blastn比对  
```
blastn -query ID_standard_CRISPRs.fasta -db GOHVGD_nuc_seq_db -task blastn-short -outfmt '6 std qlen slen' -max_target_seqs 50000000 -out ID_standard_CRISPRs_to_GOHVGD_blastn_out.txt -num_threads 1 -dust no
```

GOHMGD的MAG序列与virus contigs进行blastn比对  
```
blastn -query ID_bin.fa -db GOHVGD_nuc_seq_db -outfmt '6 std qlen slen' -max_target_seqs 50000000 -out ID_bin_long_blast.tsv -num_threads 1 -dust no
```

过滤short blastn与long blastn结果
```
python filter_short_blastn_result.py -i crt_short_blast.tsv -o filter_crt_short_blast.tsv
```
```
python filter_long_blastn_result.py -i ID_bin_long_blast.tsv -o filter_ID_bin_long_blast.tsv
```
合并short blastn与long blastn，去重后得到GOHVGD与GOHMGD的病毒-宿主分配结果
