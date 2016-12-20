#!/usr/bin/env bash

# To compare compression ratios, times, etc. between
# gzip software implementation and hardware-accelerated variants

# Usage example: ./compare_compression_fpga.sh cxidb/id22 cxidb/id22/files_to_compare.txt

# fallback to software
#GZIP_BIN="/usr/lib64/genwqe/gzip -s"
GZIP_BIN=/usr/lib64/genwqe/gzip

TIMEIT_BIN=/usr/bin/time

RAM_DISK_MPOINT=/home/common
RAM_DISK=${RAM_DISK_MPOINT}/ramdisk_150GB


gzip_disk_disk() {
    ${GZIP_BIN} < $1 > $2
}

SUMMARY_HDR="file_name, size_before_compress, size_compressed, time_disk_disk, time_ram_ram, time_ram_null"
OUT_SUMMARY=${SUMMARY_HDR}

compress_compare() {
    echo "Checking file: ${FILES_DIR}/${file}"

    IN_PATH=${FILES_DIR}/${file}
    RAM_PATH=${RAM_DISK}/${file}

    # Disk(p8:home)->compress->Disk(p8:home)
    echo "Compressing disk->disk"
    OUT_DISK_PATH=${IN_PATH}.gz
    
    #echo "timed command: ${timed_command_disk_disk}"
    time_string_disk_disk=$( { ${TIMEIT_BIN} -f '%e %U %S' ${GZIP_BIN} < ${IN_PATH} > ${OUT_DISK_PATH}; } 2>&1)
    time_vec_disk_disk=($time_string_disk_disk)
    echo "Time: ${time_string_disk_disk}, ${time_vec_disk_disk[0]}, ${time_vec_disk_disk[1]}"
    DU_OUTPUT_DISKIO=$(du -k --total --summarize  ${IN_PATH} ${OUT_DISK_PATH})
    sizes_string_disk=$(echo ${DU_OUTPUT_DISKIO} | cut -f1)
    sizes_vec=($sizes_string_disk)
    echo "Time: ${time_string_disk_disk}"
    echo "Size: ${sizes_vec[0]}, compressed: ${sizes_vec[2]}"

    rm ${OUT_DISK_PATH}


    cp ${IN_PATH} ${RAM_PATH}

    echo "Compressing RAM->RAM"
    # RAM->compress->RAM
    OUT_RAM_PATH=${RAM_PATH}.gz
    
    time_string_ram_ram=$( { ${TIMEIT_BIN} -f '%e %U %S' ${GZIP_BIN} < ${RAM_PATH} > ${OUT_RAM_PATH}; } 2>&1)
    time_vec_ram_ram=($time_string_ram_ram)
    echo "Time: ${time_string_ram_ram}"
    DU_OUTPUT=$(du -k --total --summarize  ${IN_PATH} ${OUT_RAM_PATH})
    rm ${OUT_RAM_PATH}

    echo "Compressing RAM->null"
    # RAM->compress->null
    time_string_ram_null=$( { ${TIMEIT_BIN} -f '%e %U %S' ${GZIP_BIN} < ${RAM_PATH} > /dev/null; } 2>&1)
    time_vec_ram_null=($time_string_ram_null)
    echo "Time RAM->null: ${time_string_ram_null}"

    rm ${RAM_PATH}


    echo "* Results for file ${FILES_DIR}/${file}"
    echo $SUMMARY_HDR
    summary_line="${file}, ${sizes_vec[0]}, ${sizes_vec[2]}, ${time_vec_disk_disk[0]}, ${time_vec_ram_ram[0]}, ${time_vec_ram_null[0]}"
    echo "${summary_line}"

    OUT_SUMMARY="${OUT_SUMMARY}\n${summary_line}"
}

FILES_DIR=$1
FILES_LIST=$2

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 INPUT_DATA_DIRECTORY LIST_INPUT_FILES" >&2
    exit 1
fi

if [ -z "$FILES_DIR" ] || ! [ -d "${FILES_DIR}" ]; then
    echo "First argument: provide a valid directory for input data files"
    exit 1
fi

if [ -z "${FILES_LIST}" ] || ! [ -f "${FILES_LIST}" ]; then
    echo "Second argument: provide a valid file with a list of input files"
    exit 1
fi

echo "Using data from directory: ${1}, list of files: ${2}"

STARTTIME=$(date +%s)

echo "* Start time: $(date)"
echo "* ppc64 SMT: $(ppc64_cpu --smt)"

while read file
do
    compress_compare $file
done < ${FILES_LIST}

ENDTIME=$(date +%s)

echo "Done in $(($ENDTIME - $STARTTIME)) seconds."

echo " *** Summary of results:"
echo -e "${OUT_SUMMARY}"
