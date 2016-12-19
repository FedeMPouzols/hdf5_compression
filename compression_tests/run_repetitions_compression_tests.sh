#!/usr/bin/bash
# Template to run repetitions of compression tests

# repetitions 0-159: default SMT settings
# repetitions 160-: `ppc64_cpu --smt=off`
# Note: repetitions 160-187 were done with a karabo deviceserver holding over 130GB, 
#  disk->disk tests are very slow because of lack of RAM memory for buffering
# => repeated again with free memory

DATA_ROOT=~/
OUTPUT_DIR=~/genwqe_comparison_results_hw_repetitions

i=200;

declare -a datasets=(
    "id22" 
    "id30"
)

echo "* Starting repetitions at: $(date)"

while [[ i -le 1000 ]];
do
  echo " *****************************************************************************************"
  echo " **************************** Starting repetition ${i} ***********************************"
  echo " *****************************************************************************************"
  for dset in "${datasets[@]}"
  do
      ./compare_compression_fpga.sh ${DATA_ROOT}/cxidb/${dset} ${DATA_ROOT}/cxidb/${dset}/files_to_compare_${dset}.txt | tee ${OUTPUT_DIR}/compress_comparison_results_${dset}_rep.${i}.txt
  done
  i=$((i+1));
done;
