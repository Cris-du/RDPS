# 系统发育分析
---
## Install dependencies  
### 为了进行蛋白质去冗余  
`cdhit v4.8.1`,相关配置方法可参照[cdhit](https://github.com/weizhongli/cdhit)  

### 为了进行*Caudoviricetes*标志蛋白识别  
`diamond v2.1.8`,相关配置方法可参照[diamond](https://github.com/bbuchfink/diamond?tab=readme-ov-file)  

### 为了进行*Caudoviricetes*标志蛋白聚类  
`MMseqs2 v13.4.5`,相关配置方法可参照[mmseqs2](https://github.com/soedinglab/MMseqs2)  

### 为了进行多序列比对  
`MUSCLE v5.2`,相关配置方法可参照[muscle](https://github.com/rcedgar/muscle)  

### 为了进行多序列比对结果质控  
`trimAl v1.5`,相关配置方法可参照[trimAl](https://vicfero.github.io/trimal/)  

### 为了构建*Caudoviricetes*系统发育树  
`FastTree v2.1.11`,相关配置方法可参照[fasttree](https://software.cqls.oregonstate.edu/updates/fasttree-2.1.11/)  

### 为了筛选GOHVGD/GOV2.0中完整性≥50% contig的完整蛋白质数据集  
`filter_50_compless_protein.py`  

### 你需要可以运行以下命令  
`cdhit`  
`mmseqs`  
`muscle-linux-x86.v5.2`  
`trimal`  
`FastTree`  

## 自定义脚本  
### 为了进行`GOHMGD`主要原核微生物宿主系统发育分析  
`0tree.py`  

## 执行操作  
### GOHVGD、GOV2.0、refseq数据库*Caudoviricetes*标志蛋白系统发育分析  
#### 数据准备  
对NCBI refseq (release 225)的经典*Caudoviricetes*病毒标志蛋白序列`Terl\MCP\Portal`进行去冗余  
```
cd-hit -i NCBI_refseq_terl(mcp/portal).faa -o drep_NCBI_refseq_terl(mcp/portal).faa -c 1.0 -aL 1.0 -aS 1.0 -n 5 -d 0 -T 16
```

筛选GOHVGD/GOV2.0中完整性≥50% contig的完整蛋白质数据集  
```
python ./filter_50_compless_protein.py -i GOHVGD/GOV2.0_complete_protein.faa -o GOHVGD/GOV2.0_contigs_50_completess_complete_protein.faa
```  

鉴定GOHVGD/GOV2.0中的高质量*Caudoviricetes*病毒标志蛋白`Terl\MCP\Portal`序列数据集  
```
diamond makedb --in drep_NCBI_refseq_terl(mcp/portal).faa --db ./drep_NCBI_refseq_terl(mcp/portal)_db --threads 4
```
```
diamond blastp --query GOHVGD/GOV2.0_contigs_50_completess_complete_protein.faa --db ./drep_NCBI_refseq_terl(mcp/portal).faa --out GOHVGD/GOV2.0_contigs_50_completess_complete_protein_terl(mcp/portal)_blastpout.txt --al GOHVGD/GOV2.0_contigs_50_completess_terl(mcp/portal)_complete_protein.faa --outfmt 6 --evalue 1e-5 --max-target-seqs 5000000 --threads 2
```

分别合并GOHVGD/GOV2.0以及refseq的*Caudoviricetes*病毒标志蛋白`Terl\MCP\Portal`序列文件为`terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_protein.faa`,并进行目级别聚类  
```
mmseqs easy-cluster terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_protein.faa terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_out ./terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_tmp --min-seq-id 0.269 -c 0.5 --cov-mode 1 --threads 40
```

#### 对GOHVGD/GOV2.0/refseq的`Terl\MCP\Portal`目级别代表性序列分别进行系统发育树构建  
muscle比对  
```
muscle-linux-x86.v5.2 -super5 terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_out_rep_seq.fasta -output terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster.afa -threads 10
```
trimal修剪  
```
trimal -in terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster.afa -out terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_trimal.fasta -htmlout terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_trimal.html -gappyout
```
系统发育树构建  
```
FastTree -lg terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_trimal.fasta > terl(mcp/portal)_merge_GOHVGD_GOV2.0_refseq_cluster_trimal_super5_lg_model.nwk
```

### 进行`GOHMGD`的原核微生物宿主系统发育分析  
step1    
下载gtdb release 220版本的古菌与细菌系统发育树`ar53_r220.tree`,`bac120_r220.tree`以及分类文件`ar53_taxonomy_r220.tsv`,`bac120_taxonomy_r220.tsv`  
step2  
准备`GOHMGD`已鉴定有潜在感染病毒的原核微生物宿主的分类文件  
示例:  
| domain   | layer | taxa            | genome_num |
|----------|-------|-----------------|------------|
| Bacteria | p     | Pseudomonadota   | 1313       |
| Bacteria | p     | Campylobacterota | 319        |
| Bacteria | p     | Bacteroidota     | 395        |
| Bacteria | p     | Actinomycetota   | 101        |
| Bacteria | p     | Planctomycetota  | 195        |
| Bacteria | p     | Myxococcota      | 46         |
| Bacteria | p     | Verrucomicrobiota| 32         |
| Bacteria | p     | Acidobacteriota  | 35         |

step3  
调用`0tree.py`生成主要`GOHMGD`原核微生物宿主系统发育树文件`_newick.tree`,`_nexus.tree`,`_phyloxml.tree`以及`iTOL`标签文件`ITOL_{domain}_labels_r{release}_leaf_{genome_num}.txt`  
### 使用iTOL进行系统发育树可视化  
