module load bedtools/2.25.0

data=$1

bedtools intersect -wo -a GM12878-Enhancers.bed -b $data.bed > tmp
python assign.eqtls.py ~/Lab/Reference/Human/Gencode19/Genes.bed $data.txt tmp \
    | sort -u | awk '{print $0 "\t" "Link-"NR}' > tmp1
awk 'FNR==NR {x[$7];next} ($2 in x)' \
    ~/Lab/Reference/Human/Gencode19/TSS.Filtered.bed tmp1 > $data-Links.txt
