# Defense and Anti-Defense System Analysis

---
## Install dependencies  
为了进行微生物的抗病毒系统以及病毒的抗防御系统预测  
`defense-finder v1.2.2`,相关配置方法可参照[defensefinder](https://github.com/mdmparis/defense-finder)  

你需要可以运行以下命令  
`defense-finder`  

微生物的抗病毒系统预测（实际做的是ordered，这里需要重做）  
```
defense-finder run MAG_binx.fa -o MAG_binx_defensefinder --db-type unordered_replicon -w 2
```
病毒的抗防御系统预测  
```
defense-finder run GOHVGD_virus_seq.fa -o GOHVGD_virus_antidefensefinder_dir --db-type unordered_replicon --preserve-raw -A -w 1
```
