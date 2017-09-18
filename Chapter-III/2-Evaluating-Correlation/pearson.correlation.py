import random, subprocess, numpy, sys, sklearn, scipy
from sklearn import ensemble
from sklearn.ensemble import RandomForestClassifier

def Determine_Correlation(array1, array2):
    return scipy.stats.pearsonr(array1, array2)[0]

def Create_Signal_Dict(data):
    signalDict={}
    for line in data:
        line=line.rstrip().split("\t")
        signalDict[line[0].rstrip()]=[float(i) for i in line[1:]]
    return signalDict

def Create_ELS_Dict(rdhs):
    elsDict={}
    for line in rdhs:
        line=line.rstrip().split("\t")
        elsDict[line[4].rstrip()]=line[3].rstrip()
    return elsDict

def Create_TSS_Dict(tss):
    transcriptDict={}
    geneDict={}
    for line in tss:
        line=line.rstrip().split("\t")
        transcriptDict[line[3]] = [line[0], int(line[1]), line[6]]
        if line[6] not in geneDict:
            geneDict[line[6]]=[line[3]]
        else:
            geneDict[line[6]].append(line[3])
    return geneDict, transcriptDict

positive=open(sys.argv[1])
negative=open(sys.argv[2])
m1=open(sys.argv[3])
m2=open(sys.argv[4])
tss=open(sys.argv[5])
rdhs=open(sys.argv[6])
geneDict, transcriptDict = Create_TSS_Dict(tss)
m1Signal=Create_Signal_Dict(m1)
m2Signal=Create_Signal_Dict(m2)
elsDict=Create_ELS_Dict(rdhs)
m1.close()
m2.close()
tss.close()
rdhs.close()

for line in positive:
    line=line.rstrip().split("\t")
    cor=[]
    for i in geneDict[line[1].rstrip(" ")]:
        cor.append(Determine_Correlation(m1Signal[elsDict[line[0].rstrip()]], m2Signal[i]))
    print 1, "\t", max(cor)

for line in negative:
    line=line.rstrip().split("\t")
    cor=[]
    for i in geneDict[line[1].rstrip(" ")]:
        cor.append(Determine_Correlation(m1Signal[elsDict[line[0].rstrip()]], m2Signal[i]))
    print 0, "\t", max(cor)
    
positive.close()
negative.close()
m1.close()
m2.close()
tss.close()

