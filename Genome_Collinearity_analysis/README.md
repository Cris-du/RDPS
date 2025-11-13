# Genome Collinearity analysis  
---
## Install dependencies  
### 为了进行GOHVGD ubiquitous病毒与已分离热液病毒基因组共线性检测  
`clinker-py v0.0.31`,相关配置方法可参照[clinker](https://github.com/gamcil/clinker)   

### 你需要可以运行以下命令  
`clinker`  

## 自定义脚本  
### 为了生成GOHVGD ubiquitous vOTU 代表性contig序列的`gbk`文件  
`transformat_gbk.py` 

## 执行操作
### 生成GOHVGD ubiquitous vOTU 代表性contig序列的`gbk`文件  
```
python ./transformat_gbk.py run -faa GOHVGD_ubiquitous.faa -fna GOHVGD_ubiquitous.fna -o GOHVGD_ubiquitous.gbk
```
将所有GOHVGD ubiquitous vOTU 代表性contig序列与已分离热液病毒序列`gbk`文件存放于同一目录下  
### 进行GOHVGD ubiquitous vOTU 代表性contig序列与已分离热液病毒序列共线性比对  
```
clinker clusters/*.gbk -p ubiquitous_refseq_clinker.html
```

利用`diamond blastp`将GOHVGD ubiquitous vOTU 代表性contig蛋白质序列与`PHROG`数据库蛋白质序列比对，筛选标准为`e-value ≤ 1e-5`进行蛋白质功能远缘注释，根据注释结果进行蛋白质功能分类的颜色标注(可借助adobe illustrator等工具)  
