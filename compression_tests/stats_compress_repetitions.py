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

# Define the range of repetitions to grab
rep_start = 0
max_reps = 159
fields_cnt = 5

found_cnt = 7   # this is for id22
fname_pattern = 'compress_comparison_results_id22_rep.{0}.txt'

data_root = '/home/common/fpga_tests_output'

in_data_path = 'genwqe_comparison_results_hw_repetitions'

if data_root:
    in_data_path = os.path.join(data_root, in_data_path)

results = np.zeros((max_reps, found_cnt, fields_cnt))
for rep_idx in range(rep_start, max_reps):
    # file names with repetition starting from 1...
    fname = 'compress_comparison_results_id22_rep.{0}.txt'.format(rep_idx+1)
    print('Loading results file: {0}'.format(fname))
    results[rep_idx, :, :] = load_results_file(os.path.join(in_data_path,
                                                            fname),
                                               fields_cnt)


def print_indiv_results(results, idx):
    print('Repetition idx {0}, compression ratio: {0}'.
          format(results[idx, 0, 0] / results[idx, 0, 1]))
    print('   Rate, disk I/O: {0}, GB/s'.
          format(results[idx, 0, 0] / results[idx, 0, 2]/1024/1024))
    print('   Rate, RAM I/O: {0}, GB/s'.
          format(results[idx, 0, 0] / results[idx, 0, 3]/1024/1024))
    print('   Rate, RAM I, null O: {0}, GB/s'.
          format(results[idx, 0, 0] / results[idx, 0, 4] / 1024 / 1024))


# Some checks on minimum/maximum values across all repetitions
print_indiv_results(results, 0)


def rate_info_str(rate_data):
    ''' rate_data assumed in GB/s '''
    return ('average: {0}, GB/s, stddev: {1}, min: {2}, max: {3}'.
            format(np.mean(rate_data), np.std(rate_data),
                   np.amin(rate_data), np.amax(rate_data)))


print('*** Overall results ***')
comp_ratio = results[:, 0, 0] / results[:, 0, 1]
print('Compression ratio, average: {0}, stddev: {1}'.
      format(np.mean(comp_ratio), np.std(comp_ratio)))


rate_disk_io = results[:, 0, 0] / results[:, 0, 2] / 1024 / 1024
print('   Rate, disk I/O, {0}'.
      format(rate_info_str(rate_disk_io)))

rate_ram_io = results[:, 0, 0] / results[:, 0, 3] / 1024 / 1024
print('   Rate, RAM I/O, {0}'.
      format(rate_info_str(rate_ram_io)))

rate_ram_i_null_o = results[:, 0, 0] / results[:, 0, 4] / 1024 / 1024
print('   Rate, RAM I, null O, {0}'.
      format(rate_info_str(rate_ram_i_null_o)))
