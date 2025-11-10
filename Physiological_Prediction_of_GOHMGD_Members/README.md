# Physiological Prediction of GOHMGD Members

---
## Install dependencies  
为了进行GOHMGD最适生长温度（OGT）预测  
`tome v2.0`,相关配置方法可参照[tome](https://github.com/EngqvistLab/Tome)   

为了进行GOHMGD最短倍增时间（MDT）预测  
`gRodon v1.0`,由于`gRodon`是一个R包,具体配置与使用方法参照[gRodon](https://www.microbialgamut.com/gRodon-vignette)   

你需要可以运行以下命令  
`tome`  

GOHMGD最适生长温度（OGT）预测,`bin_ID_protein.fasta`为该bin的蛋白质序列文件  
```
tome predOGT --fasta bin_ID_protein.fasta > bin_ID_ogt_out.txt
```

GOHMGD最短倍增时间（MDT）预测  
下载标准ribosomal.hmm文件,以识别GOHMGD每个bin的ribosomal序列结果  

安装好`gRodon`后，对GOHMGD的MDT预测可参照脚本内容  
```
library(gRodon)
library(Biostrings)
genes <- readDNAStringSet(".../bin_ID_orf.fna")
highly_expressed <- read.table(".../bin_ID.judge", header=TRUE, sep="\t")$judge
r <- predictGrowth(genes, highly_expressed, mode="partial")
d <- as.data.frame(r)
write.table(d, ".../bin_ID.gRodon2.txt", sep="\t")
```

