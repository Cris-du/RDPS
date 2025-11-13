library(gRodon)
library(Biostrings)
genes <- readDNAStringSet(".../bin_id_orf.fna")
highly_expressed <- read.table(".../bin_id.judge", header=TRUE, sep="\t")$judge
r <- predictGrowth(genes, highly_expressed, mode="partial")
d <- as.data.frame(r)
write.table(d, ".../bin_id.gRodon2.txt", sep="\t")
