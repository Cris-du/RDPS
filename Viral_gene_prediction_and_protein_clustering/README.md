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

使用`prodigal-gv`对GOHVGD进行病毒基因预测,设定每个样本的病毒序列文件为`sampleID_virus.fna`  
```
prodigal-gv -i sampleID_virus.fna -o sampleID_virus.gff -a sampleID_virus.faa -d sampleID_virus.fna -f gff -p meta
```  

移动所有样本的蛋白质faa文件至同一目录下,并进行合并至同一个faa文件,为`GOHVGD_protein.faa`  
```
cat *.faa > GOHVGD_protein.faa
```

使用`cd-hit`对GOHVGD的蛋白质进行聚类  
```
cd-hit -i GOHVGD_protein.faa -o GOHVGD_protein_cluster.faa -c 0.6 -aS 0.8 -g 1 -n 4 -d 0 -T 64 -M 0
```

由于原始的聚类结果文件`GOHVGD_protein_cluster.faa.clstr`内容结构非传统表格文件,如tsv,csv等,故提供`transformat_pcs_report.py`脚本以供文件格式转换,用户可酌情使用
```
python transformat_pcs_report.py -i GOHVGD_protein_cluster.faa.clstr -o GOHVGD_protein_cluster.tsv
```
