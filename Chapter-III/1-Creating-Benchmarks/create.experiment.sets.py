#Jill E. Moore
#Weng Lab
#University of Massachusetts Medical School

import sys
import subprocess

def Process_Links(links):
    linkDict={}
    for line in links:
        line=line.rstrip().split("\t")
        if line[0] in linkDict:
            linkDict[line[0]][line[1]]=line[2]
        else:
            linkDict[line[0]]={line[1]:line[2]}
    return linkDict

def Determine_Nearby_TSS(enhancer, tss, D):
    predictionDict={}
    region=open("range", "w")
    for line in open (enhancer):
        line=line.rstrip().split("\t")
        start=int(line[1])-D
        stop=int(line[2])+D
        if start < 0:
            start=0
        print >> region, line[0] + "\t"+str(start)+"\t"+str(stop)+"\t"+"\t".join(line[3:len(line)])
    region.close()
    test2=open("intersection2.bed", "w")
    print "\t intersecting enhancers and tss ..."
    subprocess.call(["bedtools", "intersect", "-wo","-a", "range", "-b", tss], stdout=test2)
    test2.close()
    test2=open("intersection2.bed", "r")
    for line in test2:
        line=line.rstrip().split("\t")
        if line[3] not in predictionDict:
            predictionDict[line[3]]=[line[15]]
        else:
            predictionDict[line[3]].append(line[15])
            predictionDict[line[3]]=list(set(predictionDict[line[3]]))
    return predictionDict
def Create_Test_Set(tsss, linkDict, blackListDict):
    positive=open("positive", "w")
    negative=open("negative", "w")
    for prediction in tsss:
        if prediction in linkDict:
            for gene in tsss[prediction]:
                if gene in linkDict[prediction]:
                    print >> positive, prediction, "\t", gene, "\t", linkDict[prediction][gene]
		elif prediction not in blackListDict:
		    print >> negative, prediction, "\t", gene
                elif gene not in blackListDict[prediction]:
                    print >> negative, prediction, "\t", gene
                
    positive.close()
    negative.close()
                    
links=open(sys.argv[1])
tss=sys.argv[2]
enhancer=sys.argv[3]
output=open(sys.argv[4], "w")
D=int(sys.argv[5])
bl=open(sys.argv[6])
print "Now processing links..."
linkDict=Process_Links(links)
blackListDict=Process_Links(bl)
print "Now determining nearby tss...."
tsss=Determine_Nearby_TSS(enhancer, tss, D)
print "Now creating test set...."
Create_Test_Set(tsss, linkDict, blackListDict)
    
output.close()
links.close()
