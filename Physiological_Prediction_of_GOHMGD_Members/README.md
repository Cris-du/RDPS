# Physiological Prediction of GOHMGD Members  
---
## Install dependencies  
### 为了进行GOHMGD MAG bin蛋白质与orf预测  
`prodigal v2.6.3`,相关配置方法可参照[prodigal](https://github.com/hyattpd/Prodigal)   

### 为了进行GOHMGD最适生长温度（OGT）预测  
`tome v2.0`,相关配置方法可参照[tome](https://github.com/EngqvistLab/Tome)   

### 为了进行GOHMGD最短倍增时间（MDT）预测  
`gRodon v1.0`,由于`gRodon`是一个R包,具体配置与使用方法参照[gRodon](https://www.microbialgamut.com/gRodon-vignette)   

### 你需要可以运行以下命令  
`prodigal`  
`tome`  
`hmmsearch`  

## 执行操作  
### 预测GOHMGD MAG bin的蛋白质与orf数据集  
```
prodigal -i bin_id.fna -o bin_id.gff -a bin_id_protein.faa -d bin_id_orf.fna -f gff -p single
```
### GOHMGD最适生长温度（OGT）预测  
```
tome predOGT --fasta bin_id_protein.faa > bin_ID_ogt_out.txt
```
### GOHMGD最短倍增时间（MDT）预测  
下载标准`KEGG`数据库的核糖体蛋白集合（br01610）`ribosomal.hmm`文件,以鉴定GOHMGD每个bin的ribosomal序列  
```
hmmsearch --tblout bin_id_vs_ribosomal_out.txt --noali -E 1e-10 --domE 1e-10 ribosomal.hmm bin_id_protein.faa
```

在`R`中安装好`gRodon`package后，将`bin_id_orf.fna`与`bin_id.judge`文件路径输入脚本`gRodon_bin_id.R`即可  
`bin_id.judge`文件包含该bin中的核糖体基因判断结果:  
| gene           | judge |
|----------------|-------|
| gene_ribosomal | TRUE  |
| gene_1         | FALSE |
| gene_2         | FALSE |
| gene_3         | FALSE |
| gene_4         | FALSE |
| gene_5         | FALSE |
