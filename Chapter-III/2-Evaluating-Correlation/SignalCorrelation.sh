source ~/.bashrc
module load R/3.1.0

data=$1
signal=$2

positive=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Benchmark/*/$data-Validation-P.txt
negative=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Benchmark/*/$data-Validation-N.txt
rDHS=~/Lab/Results/V4-hg19/hg19-cREs-Simple.bed
tss=/home/jm36w/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Benchmark/ChIA-PET/TSS.Filtered.bed
scriptDir=/home/jm36w/Projects/ENCODE/Encyclopedia/Version4/Linking-Methods/

echo "Prepping data..."
awk '{print $1}' $positive $negative | sort -u > ELS
awk 'FNR==NR {x[$1];next} ($5 in x)' ELS $rDHS | awk '{print $4}' > rDHS
awk '{print $2}' $positive $negative | sort -u > Genes
awk 'FNR==NR {x[$1];next} ($7 in x)' Genes $tss | awk '{print $4}' > TSS

echo "Creating small matrices..."
M1=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Signal-Matrix/ELS-$signal-Zscore-Matrix.txt
M2=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Signal-Matrix/TSS-$signal-Zscore-Matrix.txt

awk 'FNR==NR {x[$1];next} ($1 in x)' rDHS $M1 > m1.matrix.txt
awk 'FNR==NR {x[$1];next} ($1 in x)' TSS $M2 > m2.matrix.txt

echo "Running pearson zscore..."
python $scriptDir/pearson.correlation.py $positive $negative \
    m1.matrix.txt m2.matrix.txt $tss $rDHS > Pearson.$signal.Zscore.txt

echo "Running spearman zscore..."
python $scriptDir/spearman.correlation.py $positive $negative \
    m1.matrix.txt m2.matrix.txt $tss $rDHS > Spearman.$signal.Zscore.txt

echo "Creating small matrices..."
M1=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Signal-Matrix/ELS-$signal-Raw-Matrix.txt
M2=~/Lab/ENCODE/Encyclopedia/V4/hg19-Links/Signal-Matrix/TSS-$signal-Raw-Matrix.txt

awk 'FNR==NR {x[$1];next} ($1 in x)' rDHS $M1 > m1.matrix.txt
awk 'FNR==NR {x[$1];next} ($1 in x)' TSS $M2 > m2.matrix.txt

echo "Running pearson raw..."
python $scriptDir/pearson.correlation.py $positive $negative \
    m1.matrix.txt m2.matrix.txt $tss $rDHS > Pearson.$signal.Raw.txt

echo "Running spearman raw..."
python $scriptDir/spearman.correlation.py $positive $negative \
    m1.matrix.txt m2.matrix.txt $tss $rDHS > Spearman.$signal.Raw.txt

Rscript $scriptDir/area.under.curves.R Pearson.$signal.Raw.txt \
Pearson.$signal.Zscore.txt Spearman.$signal.Raw.txt Spearman.$signal.Zscore.txt

rm ELS Genes TSS rDHS *.matrix.txt
