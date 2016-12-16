#!/usr/bin/env python
"""
Load results for 'many' repetitions and calculate statistics of the
data rate such as maximum time or minimum rate over all the repetitions, 
average, std/variation of the rate, etc.
"""
from __future__ import print_function

import os

import numpy as np


# 'compress_comparison_results_id30_rep.{0}.txt'.format(rep_id)


# look for lines after a line like this: '*** Summary of results:'

def load_results_file(fname, fields_cnt):
    """
    Expects file_name and fields_cnt float values for every file:
    file_name, size_before_compress, size_compressed, time_disk_disk, 
    time_ram_ram, time_ram_null

    @param fields_cnt :: how many numeric fields are expected per line/file
                         (5 fields are used)
    """
    results_found = []
    found_cnt = 0
    with open(fname, 'r') as ifile:
        for line in ifile:
            if '*** Summary of results' in line:
                # skip header
                next(ifile)
                for line in ifile:
                    results_found.append(line)
                    found_cnt += 1
    print('* Found:\n{0}'.format(results_found))
    print('({0} files)'.format(found_cnt))

    results = np.zeros((found_cnt, fields_cnt))
    file_idx = 0
    for file_line in results_found:
        columns = file_line.split(',')
        print ('Results for file {0} : {1}'.format(columns[0], columns[1:]))
        results[file_idx, :] = [float(item) for item in columns[1:]]
        file_idx += 1
    return results


# 20161121: at repetition 166
max_reps = 5 #165
fields_cnt = 5


found_cnt = 7 # this is for id22
results = np.zeros((max_reps, found_cnt, fields_cnt))


in_data_path = 'genwqe_comparison_results_hw_repetitions'
fname_pattern = 'compress_comparison_results_id22_rep.{0}.txt'

rep_start = 0
for rep_idx in range(rep_start, max_reps):
    # file names with repetition starting from 1...
    fname = 'compress_comparison_results_id22_rep.{0}.txt'.format(rep_idx+1)
    print('Loading results file: {0}'.format(fname))
    results[rep_idx, :, :] = load_results_file(os.path.join(in_data_path, fname),
                                               fields_cnt)

print(results[0, :, :])

# Some checks on minimum/maximum values across all repetitions
rep_idx = 0
print('Compression ratio: {0}'.format(results[rep_idx, 0,0]/results[rep_idx, 0,1]))
print('Rate, disk I/O: {0}, GB/s'.format(results[rep_idx, 0,0]/results[rep_idx, 0,2]/1024/1024))
print('Rate, RAM I/O: {0}, GB/s'.format(results[rep_idx, 0,0]/results[rep_idx, 0,3]/1024/1024))
print('Rate, RAM I, null O: {0}, GB/s'.format(results[rep_idx, 0,0]/results[rep_idx, 0,4]/1024/1024))
