#!/usr/bin/bash
# Template to run repetitions of compression tests

# repetitions 0-159: default SMT settings
# repetitions 160-: `ppc64_cpu --smt=off`
# Note: repetitions 160-187 were done with a karabo deviceserver holding over 130GB, 
#  disk->disk tests are very slow because of lack of RAM memory for buffering

DATA_ROOT=~/
OUTPUT_DIR=~/genwqe_comparison_results_hw_repetitions

i=160;
while [[ i -le 1000 ]];
do
  echo " *****************************************************************************************"
  echo " **************************** Starting repetition ${i} ***********************************"
  echo " *****************************************************************************************"
  ./compare_compression_fpga.sh ${DATA_ROOT}/cxidb/id22 ${DATA_ROOT}/cxidb/id22/files_to_compare_id22.txt | tee ${OUTPUT_DIR}/compress_comparison_results_id22_rep.${i}.txt
  ./compare_compression_fpga.sh ${DATA_ROOT}/cxidb/id30 ${DATA_ROOT}/cxidb/id30/files_to_compare_id30.txt | tee ${OUTPUT_DIR}/compress_comparison_results_id30_rep.${i}.txt
  i=$((i+1));
done;
