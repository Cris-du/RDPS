# Viral Macro-and Micro-Diversity Analyses
---
## Install dependencies  
为了进行微观多样性计算  
`metapop v1.0`,相关配置方法可参照[metapop](https://github.com/metaGmetapop/metapop)  

你需要可以运行以下命令  
`metapop`  

对`GOHVGD`每个样本的病毒序列进行微观多样性计算,其中所有样本的`bam`文件放置于`sample_bam_dir`目录下,所有样本的病毒序列放置于`reference`目录下  
step1  
```
metapop --input_samples sample_bam_dir --reference reference -o metapop_output_sample_dir --genes GOHVGD_viral_contigs.fasta --preprocess_only --threads 8
```
step2    
```
metapop --input_samples sample_bam_dir --reference reference -o metapop_output_sample_dir --genes GOHVGD_viral_contigs.fasta --min_cov 70 --min_qual 30 --min_obs 4 --skip_preproc --no_macro --no_viz --threads 8
```  
