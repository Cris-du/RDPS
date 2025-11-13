# Viral Macro-and Micro-Diversity Analyses
---
## Install dependencies  
### 为了进行微观多样性计算  
`metapop v1.0`,相关配置方法可参照[metapop](https://github.com/metaGmetapop/metapop)  

### 你需要可以运行以下命令  
`metapop`  

## 自定义脚本  
### 为了α多样性计算(需在R中提前安装`iNEXT`包)
`iNEXT.R`  
### 为了β多样性计算(需在R中提前安装`vegan`包)
`bray_curtis.R`

## 执行操作  
### 对`GOHVGD`每个样本进行α多样性计算  
准备好各样本标准化丰度数据文件,将文件路径输入脚本`iNEXT.R`即可  
单样本标准化丰度数据文件示例:  
| vOTU ID     | Abundance        |
|-------------|------------------|
| vOTU_109905 | 728730.6891579323 |
| vOTU_6793   | 9904.907626013475 |
| vOTU_1909   | 9698.912387280581 |
| vOTU_179509 | 7012.236870623882 |

### 对`GOHVGD`每个样本进行β多样性计算  
准备好样本标准化丰度数据矩阵文件,将文件路径输入脚本`bray_curtis.R`即可  
样本标准化丰度数据矩阵文件示例:  
| sample     | vOTU_1 | vOTU_10 | vOTU_100 | vOTU_1000 |
|------------|--------|---------|----------|-----------|
| DRR093004  | 3      | 0       | 0        | 0         |
| DRR093005  | 0      | 54      | 45       | 45        |
| ERR1078300 | 0      | 5       | 46       | 0         |
| ERR1078301 | 45     | 45      | 0        | 46        |
| ERR1078302 | 45     | 45      | 34       | 0         |
| ERR1679394 | 0      | 5       | 0        | 45        |
| ERR1679395 | 0      | 45      | 55       | 0         |

### 对`GOHVGD`每个样本进行微观多样性计算
每个样本的`bam`文件放置于`sample_id_bam_dir`目录下,`GOHVGD_all_viral_contigs.fna`放置于`reference`目录下  
`metapop`预处理  
```
metapop --input_samples ./sample_id_bam_dir --reference ./reference -o metapop_output_sample_dir --preprocess_only --threads 8
```
`metapop`微观多样性计算  
```
metapop --input_samples ./sample_id_bam_dir --reference ./reference -o metapop_output_sample_dir --min_cov 70 --min_qual 30 --min_obs 4 --skip_preproc --no_macro --no_viz --threads 8
```  
