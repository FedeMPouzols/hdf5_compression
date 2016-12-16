#!/usr/bin/env python
'''
Some quick consistency/sanity checks of HDF5 files.

This is useful to compare HDF5 files generated from LCLS/XTC files
using the 'xtcConverter' device. In these files images seem to be
for example in:
/instrument/CspadElement/CxiDs1-0:Cspad-0/data
/instrument/Frame/CxiDg3-0:Opal1000-0/data

Group item values:
   <HDF5 group "/instrument/CspadElement/CxiDs1-0:Cspad-0" (14 members)>
Dataset: acq_count, with shape: (500, 1), with compression options: None
 name:  /instrument/CspadElement/CxiDs1-0:Cspad-0/acq_count
Dataset: data, with shape: (500, 2296960), with compression options: None
 name:  /instrument/CspadElement/CxiDs1-0:Cspad-0/data

'''
from __future__ import print_function

import sys

import h5py


def compare_dataset(orig_file, deriv_file, dname):
    """ Compare one dataset between the two input files. """

    print(' * Comparing dataset {0}'.format(dname))

    if not dname in orig_file:
        #raise RuntimeError
        print('===Dataset {0} not present in original file: {1}'.
              format(dname, orig_file))
        # not raising an exception now, but cannot continue here

    if not dname in deriv_file:
        #raise RuntimeError
        print('===Dataset {0} not present in derived file: {1}'.
              format(dname, orig_file))
        # not raising an exception now, but cannot continue here
        return

    ds_orig = orig_file[dname]
    ds_deriv = deriv_file[dname]

    if not ds_orig == ds_deriv:
        print('   Sizes: {0}, {1}'.format(ds_orig.size, ds_deriv.size))
        print('   Attributes: {0}, {1}'.format(ds_orig.attrs.items(),
                                               ds_deriv.attrs.items()))

        print('   Shape: {0}, {1}'.
              format(ds_orig.value.shape, ds_deriv.value.shape))
        print('   dtype: {0}, {1}'.
              format(ds_orig.value.dtype, ds_deriv.value.dtype))
        # This checks shapes and then compares element-wise
        # eq_data = np.array_equal(ds_orig.value, ds_deriv.value)
        eq_count = (ds_orig.value == ds_deriv.value).sum()

        zeros_count = (ds_orig.value == 0).sum()
        print('Zeros count: {0}'.format(zeros_count))
        tf_count = (ds_orig.value == 34).sum()
        print('34s count: {0}'.format(tf_count))

        print ('   values at [33, 44]: {0}, {1}'.
               format(ds_orig.value[33, 44], ds_deriv.value[33, 44]))

        # compare against eq_data if using array_equal() (see above)
        if not ds_orig.value.size == eq_count:
            # raise RuntimeError
            print('===Dataset values not equal! Equal elements count: {0}, '
                  'count of differing elements: {1}'.
                  format(eq_count, ds_orig.value.size-eq_count))
        else:
            print('   All data are equal. OK.')


def compare_datasets_files(orig_file, deriv_file, datasets):
    """ Compare two files, looking at a list of expected datasets. """
    for dname in datasets:
        print('* Comparing file {0} with {1}, dataset {2}'.
              format(orig_file.filename, deriv_file.filename, dname))
        compare_dataset(orig_file, deriv_file, dname)


def multi_compare_derived_files(orig_file, to_compare_fnames,
                                to_compare_datasets):
    for deriv_fname in to_compare_fnames:
        with h5py.File(deriv_fname, 'r') as deriv_file:
            compare_datasets_files(orig_file, deriv_file,
                                   to_compare_datasets)


def do_compare(orig_fname, to_compare_fnames, to_compare_datasets):
    with h5py.File(orig_fname, 'r') as orig_file:
        multi_compare_derived_files(orig_file, to_compare_fnames,
                                    to_compare_datasets)


# orig_fname = '/dev/shm/scratch/MC0017-T0000-e500-no-comp.h5'

#comp1_fname = '/dev/shm/scratch/MC0017-T0000-e500-hw-comp.h5'
#comp2_fname = '/dev/shm/scratch/MC0017-T0000.h5'
#comp3_fname = '/dev/shm/scratch/MC0073-T0000.h5'
#comp4_fname = '/dev/shm/scratch2/MC0017-T0000-e500.compression.h5py.hw.h5'

#img_dataset1 = '/instrument/CspadElement/CxiDs1-0:Cspad-0/data'
#img_dataset2 = '/instrument/Frame/CxiDg3-0:Opal1000-0/data'

orig_fname = '/dev/shm/scratch/MC0027-T0000-e500-no-comp.h5'

comp1_fname = '/dev/shm/scratch/MC0027-T0000-e500-c=16k2-hw.h5'
comp2_fname = '/dev/shm/scratch/MC0027-T0000-e500-c=16k-hw.h5'
comp3_fname = '/dev/shm/scratch/MC0027-T0000-e500-c=1m-hw.h5'
comp4_fname = '/dev/shm/scratch/MC0027-T0000-e500-c=64k-hw.h5'
comp5_fname = '/dev/shm/scratch/MC0027-T0000-e500-c=e-hw.h5'

img_dataset1 = '/instrument/CspadElement/CxiDs1-0:Cspad-0/data'
img_dataset2 = '/instrument/Frame/CxiDg4-0:Tm6740-0/data'

to_compare_fnames = [comp1_fname, comp2_fname, comp3_fname, comp4_fname]
to_compare_datasets = [img_dataset1, img_dataset2]


if __name__ == "__main__":
    do_compare(orig_fname, to_compare_fnames, to_compare_datasets)
    sys.exit('Finished without issues')
