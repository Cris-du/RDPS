# Uniqueness and cross-Dataset Comparison of GOHVGD
---
## 自定义脚本    
### 为了分配独特性与共享的vOTU,PC,genus与family结果  
`tiqu_belong.py`  

## 执行操作  
### 准备vOTU,PC,genus与family成员的来源数据集文件`vOTU(pc/genus/family)_seq_belong.txt`  
| seq name | source        |
|----------|---------------|
| seq1     | GOHVGD        |
| seq2     | GOV2.0        |
| seq3     | HVG-2025        |
| seq4     | HVG-2022        |

### 准备vOTU,PC,genus与family的聚类文件`vOTU(pc/genus/family)_cluster_seq_map.txt`  
| cluster name | seq members        |
|----------|---------------|
| vOTU(pc/genus/family)1     | seq1&seq2&seq3        |
| vOTU(pc/genus/family)2     | seq4        |
| vOTU(pc/genus/family)3     | seq5&seq6        |
| vOTU(pc/genus/family)4     | seq7        |

vOTU,PC,genus与family的聚类方法分别参照[vOTU](https://github.com/Cris-du/RDPS/blob/main/Viral_prediction_and_vOTU_clustering/README.md),[PC](https://github.com/Cris-du/RDPS/blob/main/Viral_ORF_prediction_and_protein_clustering/README.md),[genus与family](https://github.com/Cris-du/RDPS/blob/main/Viral_taxonomic_assignment/README.md)  

### 识别vOTU,PC,genus与family的成员来源,以确认每个聚类的数据集独特性与共享性  
```
python ./tiqu_belong.py -it vOTU(pc/genus/family)_seq_belong.txt -iv vOTU(pc/genus/family)_cluster_seq_map.txt -o vOTU(pc/genus/family)_belong_where.txt
```
