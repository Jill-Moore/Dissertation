
args <- commandArgs(trailingOnly = TRUE)
d=read.table(args[1])
quantile(d$V3,0.95)
