# Viral Macro-and Micro-Diversity Analyses
---
## Install dependencies  
为了进行微观多样性计算  
`metapop v1.0`,相关配置方法可参照[metapop](https://github.com/metaGmetapop/metapop)  
宏观多样性计算安装R包`iNEXT`,自定义脚本  
`iNEXT.R`  

你需要可以运行以下命令  
`metapop`  

对`GOHVGD`每个样本的病毒序列进行宏观多样性计算,需要准备好样本标准化丰度数据文件,将文件路径输入脚本`iNEXT.R`即可  
标准化丰度数据文件示例:  
| vOTU ID     | Abundance        |
|-------------|------------------|
| vOTU_109905 | 728730.6891579323 |
| vOTU_6793   | 9904.907626013475 |
| vOTU_1909   | 9698.912387280581 |
| vOTU_179509 | 7012.236870623882 |

对`GOHVGD`每个样本的病毒序列进行微观多样性计算,其中每个样本的`bam`文件放置于`sample_id_bam_dir`目录下,所有样本的病毒序列放置于`reference`目录下  
step1  
```
metapop --input_samples ./sample_id_bam_dir --reference ./reference -o metapop_output_sample_dir --preprocess_only --threads 8
```
step2    
```
metapop --input_samples ./sample_id_bam_dir --reference ./reference -o metapop_output_sample_dir --min_cov 70 --min_qual 30 --min_obs 4 --skip_preproc --no_macro --no_viz --threads 8
```  
