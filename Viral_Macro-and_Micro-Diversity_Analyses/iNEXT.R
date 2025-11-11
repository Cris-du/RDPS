library(iNEXT)
data_name <- "DRR093002"
input_file <- "/dssg/home/acct-trench/trench-6/wangyecheng/Global_Hydrothermal/macrodiversity_20250405/votu_normalized_depth_by_reads_4iNEXT/DRR093002.txt"
output_file1 <- "/dssg/home/acct-trench/trench-6/wangyecheng/Global_Hydrothermal/macrodiversity_20250405/iNEXT/output/result_iNEXT_DRR093002.Rdata"
output_file2 <- "/dssg/home/acct-trench/trench-6/wangyecheng/Global_Hydrothermal/macrodiversity_20250405/iNEXT/output/result_iNEXT_DRR093002.txt"
data <- read.table(input_file, row.names=1, header=T, sep="\t")
out <- iNEXT(data, q=0, datatype="abundance")
data <- out$AsyEst
save(out,file=output_file1)
write.table(data,file=output_file2,sep = "\t",row.names=TRUE)
warnings()
