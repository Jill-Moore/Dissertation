
import sys

def Create_Gene_Dict(genes):
    geneDict={}
    for line in genes:
        line=line.rstrip().split("\t")
        geneDict[line[6]]=line[3]
        geneDict[line[3].split(".")[0]]=line[3]
    return geneDict

def Create_eQTL_Dict(eqtls):
    eqtlDict={}
    for line in eqtls:
        line=line.rstrip().split("\t")
        eqtlDict[line[0].rstrip()]=line[1].split(",")
    return eqtlDict

genes=open(sys.argv[1])
geneDict=Create_Gene_Dict(genes)
genes.close()

eqtls=open(sys.argv[2])
eqtlDict=Create_eQTL_Dict(eqtls)
eqtls.close()

intersection=open(sys.argv[3])

for line in intersection:
    line=line.rstrip().split("\t")
    for gene in eqtlDict[line[13]]:
        try:
            print line[3]+"\t"+geneDict[gene]
        except:
            pass



    

