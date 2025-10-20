# Uniqueness and cross-Dataset Comparison of GOHVGD
---
## Install dependencies  
为了标准化vOTU,PC,genus与family结果  
`standard_map_result.py`  

为了分配独特性与共享的vOTU,PC,genus与family结果  
`tiqu_belong.py`  

构建不同来源环境的contigs与蛋白质比对文件  
表格：seq1,gohvgd...  

分别标准化vOTU,PC,genus与family结果  
```
python standard_map_result.py -m votu -it contigs_belong.txt -iv vOTU_map_cluster.tsv -o vOTU_standard_map_where.txt
```  
```
python standard_map_result.py -m protein -it protein_belong.txt -iv pc_map_cluster.tsv -o pc_standard_map_where.txt
```  
```
python standard_map_result.py -m mcl -it contigs_belong.txt -iv genus_map_cluster.tsv/family_map_cluster.tsv -o genus_standard_map_where.txt/family_standard_map_where.txt
```  

识别vOTU,PC,genus与family的成员来源,以确认独特性与共享性  
```
python tiqu_belong.py -i vOTU/pc/genus/family_standard_map_where.txt -o vOTU/pc/genus/family_belong_where.txt
```
