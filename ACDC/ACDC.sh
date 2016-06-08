#!/bin/bash
#$ -cwd
#$ -pe smp 4
#$ -l h_vmem=16G

if [ $# -ne 1 ]
then
        echo "Usage: <I need a list of project and sample id>"
        exit 65
fi

module load python/2.7.8


python \
/nethome/dlin/cancer_alliance/druggability.py $1


mapfile -t array <processed_files.txt


#if [[ "${array[0]}" == *"Project_CLIR"*]]
#then
python -c 'import sys;print "".join(sorted(set.union(*[set(open(a).readlines()) for a in sys.argv[1:]])))' "${array[0]}" "${array[2]}" "${array[4]}" > "${array[0]}".W-E-P_union.txt

python -c 'import sys;print "".join(sorted(set.union(*[set(open(a).readlines()) for a in sys.argv[1:]])))' "${array[9]}" "${array[11]}" "${array[13]}" > "${array[9]}".W-E-P_union.txt

python -c 'import sys;print "".join(sorted(set.union(*[set(open(a).readlines()) for a in sys.argv[1:]])))' "${array[1]}" "${array[3]}" > "${array[0]}".CNV_union.txt

python -c 'import sys;print "".join(sorted(set.union(*[set(open(a).readlines()) for a in sys.argv[1:]])))' "${array[10]}" "${array[12]}" > "${array[10]}".CNV_union.txt
#fi

echo -e "Sample_T-N_PAIR\tCHR:POS\tREF\tALT\tGENE\tVARIANT\tSNPEFF_EFFECT\tVAF\tTOTAL_READ_COUNT\tCALLER\tTALT_COINT\tTREF_COUNT\tNALT_COUNT\tNREF_COUNT\tTIER" | cat - "${array[0]}".W-E-P_union.txt > /tmp/out && mv /tmp/out "${array[0]}".WEP_union.txt
echo -e "Sample_T-N_PAIR\tCHR:POS\tREF\tALT\tGENE\tVARIANT\tSNPEFF_EFFECT\tVAF\tTOTAL_READ_COUNT\tCALLER\tTALT_COINT\tTREF_COUNT\tNALT_COUNT\tNREF_COUNT\tTIER" | cat - "${array[9]}".W-E-P_union.txt > /tmp/out && mv /tmp/out "${array[9]}".WEP_union.txt


rm "${array[0]}".W-E-P_union.txt
rm "${array[9]}".W-E-P_union.txt