library(vegan)
library(ggplot2)
library(ade4)

subname <- "high_quality"
subname <- "total"
otu <- read.table(paste("result_abundance_matrix_4pcoa_", subname, ".txt", sep=""),row.names=1, header=T, sep="\t")


dist <- vegdist(otu,method='bray')
save(dist,file=paste("pcoa_dist_bray_by_reads_",subname,".Rdata",sep=""))
dist_table <- as.matrix(dist)
write.table(dist_table,file=paste("pcoa_dist_bray_by_reads_",subname,".txt",sep=""),sep = "\t",row.names=T, quote=FALSE)   # 输出后手动fmt一下第一列抬头
