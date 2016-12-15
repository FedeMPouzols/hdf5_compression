#!/usr/bin/env python
'''
Produces compressed HDF5 files from input/uncompressed HDF5 files.
Takes an input HDF5 file and reproduces the same structure in an
output file. The output file will have the same hierarchy, groups
and datasets but modified (enabled) compression option for some
datasets (for example those bigger than a certain threshold).
The modification is done in the function rewrite_h5_group()

Run it for example like this:
./compress_in_out_h5py.py cxidb/id30/cxidb-30.cxi out.h5
'''
from __future__ import print_function

import sys

import h5py


def add_attributes(item, item_source):
    """
    Add all the attrs from item_source as attributes in item, where
    item_source can be a group or a dataset.
    """
    for name, value in item_source.attrs.iteritems():
        item.attrs.modify(name, value)


def rewrite_h5_group(item_name, item_val, out_grp):
    if isinstance(item_val, h5py.Dataset):
        print(' dataset: {0}, with shape: {1}, with compression options: {2}'.
              format(item_name, item_val.shape, item_val.compression_opts))

        CHUNK_BLOCK = (10, 1000)
        # arbitrary minimum dataset size to enable compression
        MIN_COMPRESS_SIZE = CHUNK_BLOCK[0]*CHUNK_BLOCK[1]

        print('  name: ', item_val.name)
        if item_val.dtype == 'O':
            # Silently skip some unknown/undecided types in HDF5 file produced
            # by XTC conversion tools, etc.
            ds = None
        elif item_val.value.size >= MIN_COMPRESS_SIZE:
            # rewrite into output file enabling compression
            ds = out_grp.create_dataset(item_name, shape=item_val.shape,
                                        data=item_val.value,
                                        chunks=CHUNK_BLOCK,
                                        compression='gzip')
        else:
            # not worth compressing
            ds = out_grp.create_dataset(item_name, shape=item_val.shape,
                                        data=item_val.value)

        if ds:
            add_attributes(ds, item_val)

    elif isinstance(item_val, h5py.Group):
        print('Group: ', item_name)
        out_grp = out_grp.create_group(item_name)
        try:
            print('Group item val: ', item_val)
        except UnicodeDecodeError:
            # sometimes we get weird characters
            pass

        # set attributes?
        # out_grp.attrs = item_val.attrs
        add_attributes(out_grp, item_val)
        for subitem_name, subitem_val in item_val.items():
            rewrite_h5_group(subitem_name, subitem_val, out_grp)

    else:
        raise RuntimeError('*** Found an item that is not a group '
                           'nor a dataset. Item name: {0}. This '
                           'should not happen! ***'. format(item_name))


def rewrite_h5(in_file, out_file):
    for item_name, item_val in in_file.iteritems():
        rewrite_h5_group(item_name, item_val, out_file.parent)


def rewrite_in_to_out(in_fname, out_fname):
    with h5py.File(in_fname, 'r') as in_file:
        with h5py.File(out_fname, 'w') as out_file:
            rewrite_h5(in_file, out_file)

if 3 != len(sys.argv):
    print('Give just input and output file')
    sys.exit(-1)

print('Loading from: {0}'.format(sys.argv[1]))
print('Writing to: {0}'.format(sys.argv[2]))


if __name__ == "__main__":
    rewrite_in_to_out(sys.argv[1], sys.argv[2])
