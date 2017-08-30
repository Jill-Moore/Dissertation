import sys

def Create_Signal_Dict(signal):
    signalDict={}
    for line in signal:
        line=line.rstrip().split("\t")
        signalDict[line[0]]=float(line[4])
    return signalDict

def Create_Expression_Dict(rnaseq):
    expressionDict={}
    rnaseq.next()
    for line in rnaseq:
        line=line.rstrip().split("\t")
        expressionDict[line[0]]=float(line[6])
    return expressionDict

# def Create_Peak_Dict(peaks):
#     peakDict={}
#     tDict={}
#     finalPeakDict={}
#     for line in peaks:
#         line=line.rstrip().split("\t")
#         if line[3] not in peakDict:
#             peakDict[line[3]]=[line[11]]
#         else:
#             peakDict[line[3]].append(line[11])
#         if line[11] in tDict:
#             if float(line[7]) > tDict[line[11]][2]:
#                 tDict[line[11]]=[line[3], float(line[6]), float(line[7])]
#             elif float(line[7]) == tDict[line[11]][2] and float(line[6]) > tDict[line[11]][1]:
#                 tDict[line[11]]=[line[3], float(line[6]), float(line[7])]
#         else:
#             tDict[line[11]]=[line[3], float(line[6]), float(line[7])]
#     for t in tDict:
#         finalPeakDict[tDict[t][0]]=peakDict[tDict[t][0]]
#     return finalPeakDict

def Create_Peak_Dict(peaks):
    gDict={}
    for line in peaks:
        line=line.rstrip().split("\t")
        if line[6] not in gDict:
            gDict[line[6]]=[line[11]]
        elif line[11] not in gDict[line[6]]:
            gDict[line[6]].append(line[11])
    return gDict



rnaseq=open(sys.argv[1])
peaks=open(sys.argv[2])
dnase=open(sys.argv[3])
h3k4me3=open(sys.argv[4])

expressionDict=Create_Expression_Dict(rnaseq)
gDict=Create_Peak_Dict(peaks)
dnaseDict=Create_Signal_Dict(dnase)
h3k4me3Dict=Create_Signal_Dict(h3k4me3)


for entry in gDict:
    D=0
    H=0
    try:
        for cre in gDict[entry]:
            D += dnaseDict[cre]
            H += h3k4me3Dict[cre]
        print entry, "\t", expressionDict[entry], "\t", D/float(len(gDict[entry])), "\t", H/float(len(gDict[entry]))
    except:
        pass
rnaseq.close()
peaks.close()
dnase.close()
h3k4me3.close()


