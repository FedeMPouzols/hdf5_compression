
#Tests of the GenWQE/PCIe Accelerator for the European XFEL

## Summary

This document gives an overview of the tests done for the evaluation
of the GenWQE PFGA accelerator as part of the data management system
of the European XFEL. It also provides examples, links and comments to
reproduce these tests and perform future tests.

### Prerequisites

* Access to the test machine p8.desy.de

* Access to the [Karabo framework and related
repositories](https://git.xfel.eu/gitlab/Karabo/)

* Familiarity with the Eu.XFEL ITDM setup. Useful resources include:
  - Slides for the ITDM advisory committee, December 2016
  - Slides for Karabo 2.0 workshop, 19th December 2016

* Familiarity with the IBM FPGA accelerator for GZIP compression, see
for example this [presentation for
DESY](CAPI_GENWQE-GZIP_for_DESY.pdf), and additional documents and
links given below

## Conclusions from tests run before January 2017.

Test results performed primarily on XTC files from the
[LCLS](https://lcls.slac.stanford.edu) were presented and discussed
with IBM experts in a workshop held on the 23rd of October, 2016.  A
summary is available in [these slides,
slides_compression_gzip_fpga_evaluation_ibm_workshop](docs/slides_compression_gzip_fpga_evaluation_ibm_workshop.pdf).
As of the end of December 2016 the following conclusions seem valid:

- Rates of the order of GB/s [0.8, 1.1] are consistently delivered by
  the P8/GenWQE FPGA device. Software implementations can barely
  deliver rates of the order of 10 MB/s (between 10 and 40 depending
  on data pattern, platform, compiler, etc.).

- Storage saving of [30, 50]% possible for hard to compress data files
  (XTC files from LCLS). This could be considered as a pessimistic
  estimate.

- Storage saving >90% or even >95% possible for HDF5 files converted
  from XTC files. This could be seen as an optimistic estimate. 

The only reservation about the optimistic, >90% saving, estimate is
that by inspecting the images in these files one can observe that they
are mostly "empty" without any background or noise. it will be
possible to compress Eu.XFEL images with large storage saving to the
extent to which Eu.XFEL sensors produce similarly compressible
patterns (or the raw sensor data can be processed to produce similarly
compressible patterns).

## Next points to evaluate

- Images from Eu.XFEL sensors, what they look like and what
  compression ratios are possible. This should shed some light on
  whether the storage saving will be closer to the worse case
  ([30,50]%) or the best case (>90%).

- [GPFS](www.ibm.com/support/knowledgecenter/SSFKCN/gpfs_welcome.html). Is
  it fast enough that will not produce a bottleneck for processes
  writing files at a rate of the order of a GB/s?

## Experimental datasets

Dr. Adrian Mancuso suggested three types of datasets:

* Sequential crystallography
* Not-so-weakly scattering
* Weakly scattering 

Raw data for these types of experiments can be retrieved from the
[Coherent X-ray Imaging Data Bank, CXIDB](http://cxidb.org).

The test raw files used as of December 2016 correspond to two datasets:

* [Dataset CXIDB 22](http://cxidb.org/id-22.html) - for sequential
  crystallography, beamline CXI of the LCLS.
* [Dataset CXIDB 30](http://cxidb.org/id-30.html) - for Not-so-weakly
  scattering, beamline AMO of the LCLS.

Further data for the weakly scattering type of experiment can be
provided by instrument scientists in the future. Some of the raw data
files analyzed for which the storage saving can be >90% were acquired
with the CSPad (Cornell-SLAC Pixel Array Detector) at LCLS. Details on
how the experiments are performed and the resulting data deposited on
the CXIDB can be found in White et al. (2016).


[WhiteEtAl206](http://www.nature.com/articles/sdata201657?WT.feed_name=subjects_physical-sciences)
White et al. 2016. Serial femtosecond crystallography datasets from G
protein-coupled receptors. Scientific Data 3, Article number:
160057. doi: 10.1038/sdata.2016.57.

The raw data files are provided in [XTC
format](https://confluence.slac.stanford.edu/display/PSDM/The+XTC+to+HDF5+Translator).
Djelloul can provide further details about this format, and explain
the use of the Karabo device `xtcConverter` which is available on
p8.desy.de. This device can produce HDF5 files from some of the of the
CXIDB raw data XTC files.


## Using the GenWQE/PCIe accelerator

This accelerator implements the standard [DEFLATE
algorithm](http://www.zlib.net/feldspar.html) and is a drop-in
replacement for the common software implementation via dynamic
linking. The next sections highlight some important points on how to
set it up and some performance considerations relevant to our
application area.

Comprehensive documentation for this product is available in the
[CAPI accelerated GZIP Compression Adapter User's guide from IBM](docs/CAPI-GZIP-Usersguide.pdf) which is made
available online on the [Linux on Power community
website](https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/W51a7ffcf4dfd_4b40_9d82_446ebc23c550/page/CAPI%20accelerated%20GZIP%20Compression%20Adapter%20User%E2%80%99s%20guide).

The software, user tools and library, are open source and available as
[project genwqe-user on
GitHub](https://github.com/ibm-genwqe/genwqe-user).

The software packages for [RHEL
7](https://access.redhat.com/products/red-hat-enterprise-linux) on
Power systems can be found in this list of [packages for
RHEL7](http://public.dhe.ibm.com/software/server/POWER/Linux/yum/OSS/RHEL/7/ppc64le/). These
packages are installed ion p8.desy.de.

* The data files downloaded from the [CXIDB](http://cxidb.org) are
  availble under `p8.desy.de:/home/common/cxidb`


### Using environment variables

Example commands to run shell processes with FPGA acceleration:

```
ZLIB_ACCELERATOR=GENWQE LD_PRELOAD=/usr/lib64/genwqe/libz.so.1 /usr/bin/time -f '%e %U %S' /usr/bin/genwqe_gzip < ramdisk_150GB/e239-r0028-s00-c00.xtc > ramdisk_150GB/e239-r0028-s00-c00.xt\
c.gz
```

See more details below and in the example scripts
`compare_compression_fpga.sh` and
`run_repetitions_compression_tests.sh`.


Note that when using the FPGA accelerator the compression level
parameter will be ignored, as the FPGA implements only one variant or
level.

### Logs/trace from FPGA

A trace with different levels of details is produced into the standard
output when specifying the environment variable `ZLIB_TRACE`. For
example:

```
ZLIB_TRACE=0x08 ZLIB_ACCELERATOR=GENWQE LD_PRELOAD=/usr/lib64/genwqe/libz.so.1 /usr/bin/time -f '%e %U %S' /usr/bin/genwqe_gzip < ramdisk_150GB/e239-r0028-s00-c00.xtc > ramdisk_150GB/e239-r0028-s00-c00.xtc.gz
```
Will produce a summary:
```
Info: deflateInit: 1
Info: deflate: 1050139 sw: 0 hw: 1050139
Info:   deflate_avail_in    4 KiB: 296443
Info:   deflate_avail_in   40 KiB: 1
Info:   deflate_avail_in  132 KiB: 753695
Info:   deflate_avail_out  132 KiB: 1050139
Info:   deflate_total_in 1024 KiB: 1
Info:   deflate_total_out 1024 KiB: 1
Info: deflateSetHeader: 1
Info: deflateEnd: 1
Info: inflateInit: 0
Info: inflate: 0 sw: 0 hw: 0
...
```

The level of detail of the output can be set with the value of the
ZLIB_TRACE option, see section 5 - Application Enablement of the [CAPI
accelerated GZIP Compression Adapter User's
guide](docs/CAPI-GZIP-Usersguide.pdf). In particular `ZLIB_TRACE=0x08`
will generate a very verbose deflate/compression log.


### Using acceleration with custom code/tools

For an example of custom compression tool implemented in C see [code
of the zlib example](http://www.zlib.net/zlib_how.html)), or section
4.3 Zpipe - Example zlib application of the [CAPI accelerated GZIP
Compression Adapter User's guide](docs/CAPI-GZIP-Usersguide.pdf).

### Other compression tools/algorithms (software implementations).

Other alternatives, in particular the
[lz4](https://github.com/lz4/lz4) compression algorithm software
implementation are briefly explored
[here](other_compression_algorithms.md).


### Compression filters in HDF5

[Compression
filters](http://docs.h5py.org/en/latest/high/dataset.html#filter-pipeline)
enable compression when writing datasets in HDF5 files via the HDF5
library. Several lossless compression methods are supported, and
additional plugins are available. Here we are interested in the *GZIP
filter*.

#### Karabo HDF5 API

When using the Karabo HDF5 API, HDF5 compression can be enabled by
using the method `karabo::io::h5::Element::setCompressionLevel(int)` ,
or just by setting the `compressionLevel` option in the data format
parameter passed to the method `createTable()` of the HDF5 `File`
class: `karabo::io::h5::File::createTable(const std::string&, const
Format::Pointer)`. See an example in the file
[H5File_Test.cc](H5File_Test.cc), modified from the `io` unit tests of
Karabo, test
[H5File_Test](https://git.xfel.eu/gitlab/Karabo/Framework/blob/master/src/karabo/tests/io/H5File_Test.cc)).
Note again that the specific compression level is ignored/irrelevant
when using the FPGA accelerator.

Note that Karabo is not officially supported on the IBM Power
platform. The dependencies of Karabo [are not
available](http://exflserv05.desy.de/karabo/karaboDevelopmentDeps/)
and need to be compiled manually.

* A Karabo package is available on p8.desy.de, under
  /home/common/karabo/Framework. This is a package built from sources
  ([Framework
  repository](https://git.xfel.eu/gitlab/Karabo/Framework/). These
  sources include the required modifications to compile Karabo on
  RHEL7/Power8.


#### Python, h5py

An example of HDF5 compression can be found in
[`compress_hdf5_in2out.py`](compress_hdf5_in2out.py). 

An example of manipulation of HDF5 files is in
check_compressed_xtc_converter_h5_files.py

Both examples use the widespread [h5py
package](http://docs.h5py.org/en/latest/high/dataset.html#filter-pipeline).

#### Inspecting the data (images) in HDF5 files converted from XTC/LCLS raw data files

The structure of these HDF5 can vary. Exploring them with an
interactive Python interpreter and h5py is a convenient alternative,
in addition to the traditional HDF5 tools and helpers. A simple
example that retrieves some groups and datasets and plots some images
can be found in
[`example_plot_hdf5_xtc_lcls.py`](example_plot_hdf5_xtc_lcls.py).

#### Data in CXI (HDF5) files

For [Dataset CXIDB 30](http://cxidb.org/id-30.html), in addition to
the raw data files, a "Diffraction Pattern" file is provided. This
file is in [CXI format](http://cxidb.org/cxi.html) which is HDF5,
following the [NeXus](http://www.nexusformat.org/) approach and
partially compatible with NeXus. This type of file can be inspected
with standard HDF5 tools, such as
[HDFView](https://support.hdfgroup.org/products/java/hdfview/) or [HDF
Explorer](https://github.com/pedro-vicente/hdf-explorer), or with
scripts like the example_plot_hdf5_xtc_lcls.py example given
above. 

This file can be compressed with the example script
compress_hdf5_in2out.py given above, similarly as the HDF5 files
converted from raw data XTC files. The compression ratio for this CXI
file is ~12.0 with standard software GZIP, and ~7.15 with accelerated
compression. Note that the file contains easily compressible
information such as image masks.


## Running tests

Can be run using the [gzip tool distributed with
GenWQE](https://github.com/ibm-genwqe/genwqe-user/tree/master/tools)
or custom tools (for example the using the [code of the zlib
example](http://www.zlib.net/zlib_how.html)).

Other [tests included with the genwqe-user
package](https://github.com/ibm-genwqe/genwqe-user/blob/master/misc/ratio_test.sh).

Note: when using environment variables for processes, the variable
`ZLIB_ACCELERATOR` can be used to make sure that a particular type of
acceleration is selected.
```
ZLIB_ACCELERATOR=GENWQE LD_PRELOAD=/usr/lib64/genwqe/libz.so.1
```
For CAPI-enabled cards the alternative option is `ZLIB_ACCELERATOR=CAPI`.

This is used in the command line for example like this:
```
ZLIB_ACCELERATOR=GENWQE LD_PRELOAD=/usr/lib64/genwqe/libz.so.1 ./binary
```

The script
[compare_compression_fpga.sh](compression_tests/compare_compression_fpga.sh)
which can be used for example like this for raw XTC files:

```
./compare_compression_fpga.sh cxidb/id22 cxidb/id22/files_to_compare_id22.txt |tee compress_comparison_results_id22.txt
./compare_compression_fpga.sh cxidb/id30 cxidb/id30/files_to_compare_id30.txt |tee compress_comparison_results_id30.txt
```

Or also for HDF5 files, including CXI files:
```
./compare_compression_fpga.sh cxidb/id30 cxidb/id30/data_files_to_compare_cxi.txt | tee compress_comparison_data_cxi_results_id30.txt
```

This script runs commands using the environment variable approach, like for example:
```
ZLIB_ACCELERATOR=GENWQE LD_PRELOAD=/usr/lib64/genwqe/libz.so.1 /usr/bin/time -f '%e %U %S' /usr/bin/genwqe_gzip < ramdisk_150GB/e239-r0028-s00-c00.xtc > ramdisk_150GB/e239-r0028-s00-c00.xtc.gz
```


### Comparison criteria

The scripts report a number of results and statistics. Among these,
performance can be summarized in terms of space saving and speed of
compression using the two following metrics:

* Space saving, defined as

```
space_saving = 1 – 1/comp_ratio
```
where the [data compression ratio](https://en.wikipedia.org/wiki/Data_compression_ratio), `comp_ratio` is:
```
comp_ratio =  uncompressed_size / compressed_size
```

* Data compression rate (speed), measured as the total size of the
  uncompressed file divided by the time required to produced a
  compressed stream or file. 

This can be measured using Disk I/O, different forms of memory I/O, or
a combination of them.


### Multiple repetitions

The script
[run_repetitions_compression_tests.sh](compression_tests/run_repetitions_compression_tests.sh)
is an example that can be used To run multiple repetitions of
compression tests with multiple datasets. This can be used for example
to run tests on all the available [CXIDB](http://cxidb.org) raw data
files. This essentially runs a loop that uses the script
[compare_compression_fpga.sh](compression_tests/compare_compression_fpga.sh)
with a given list of files to compare and produces output text files:

```
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
```

A collection of test results is available on p8 under
`/home/common/fpga_tests_output`

These were used to produce some of the results shown in
[slides_compression_gzip_fpga_evaluation_ibm_workshop](docs/slides_compression_gzip_fpga_evaluation_ibm_workshop.pdf),
[`compression_comparison_results_dec2016.ods`](compression_tests/compression_comparison_results_dec2016.ods)
and other documents.


### Multi-thread/process compression

The FPGA accelerator support multi-thread applications and multiple
simultaneous processed. 

The performance with multiple thread can be evaluated as in the the
genwqe [mt performance
tests](https://github.com/ibm-genwqe/genwqe-user/wiki/Explore%20performance%20with%20genwqe_mt_perf),
with different files, or in the simplest setup starting multiple
processed simultaneously, see the following examples:

```
# multi-thread/process, ~4.5 GB - cxidb/id22/e239-r0027-s00-c00.xtc
/usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip   < cxidb/id22/e239-r0027-s00-c00.xtc > ~/ramdisk_150GB/comp.gz & /usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip  < cxidb/id22/e239-r0027-s01-c00.xtc > ~/ramdisk_150GB/comp2.gz &

#  ~95 GB - cxidb/id22/e239-r0028-s00-c00.xtc
/usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip   < cxidb/id22/e239-r0028-s00-c00.xtc > ~/ramdisk_150GB/comp.gz & /usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip  < cxidb/id22/e239-r0028-s00-c00.xtc > ~/ramdisk_150GB/comp2.gz &

# ~56 GB - cxidb/id22/e239-r0028-s00-c01.xtc
/usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip   < cxidb/id22/e239-r0028-s00-c01.xtc > ~/ramdisk_150GB/comp.gz & /usr/bin/time -f '%e %U %S' /usr/lib64/genwqe/gzip  < cxidb/id22/e239-r0028-s00-c01.xtc > ~/ramdisk_150GB/comp2.gz &
```


## Results and statistics

The comparison scripts generate text files with a detailed log which
also includes a section with numerical results (in csv format).  The
comparison results and statistics about storage saving and compression
speed can be parsed and processed like in the example script
[`stats_compress_repetitions.py`](compression_tests/stats_compress_repetitions.py).
These can be then collated, summarized and compared in a spreadsheet,
as in the file
[`compression_comparison_results_dec2016.ods`](compression_tests/compression_comparison_results_dec2016.ods).


## Performance considerations

### CPU load

A concern, especially with non-CAPI FPGA accelerators, is that the CPU
load could be high for some datasets, compromising the performance or
throughput of the accelerator. In principle , in the tests provided
with the [genwqe-user
software](https://github.com/ibm-genwqe/genwqe-user) or the tests done
with [CXIDB](http://cxidb.org) raw data files.

Screenshots [p8_screenshot_htop](p8_screenshot_htop.png) and
[p8_screenshot_htop_2](p8_screenshot_htop_2.png)

Note that an additional factor with a (lesser) influence on the
compression ratio is the HDF [chunk
size][https://support.hdfgroup.org/HDF5/doc/Advanced/Chunking/]


### Power8 hyperthreading

The command line tool `ppc64_cpu` can be used to setup Simultaneous
multithreading (SMT) / Hyperthreading on Power8 systems. Power8 has a
SMT capability of 8 threads per core. Example help output from the
tool:

```
% ppc64_cpu --help
Usage: ppc64_cpu [command] [options]
ppc64_cpu --smt                     # Get current SMT state
ppc64_cpu --smt={on|off}            # Turn SMT on/off
ppc64_cpu --smt=X                   # Set SMT state to X

ppc64_cpu --cores-present           # Get the number of cores present
ppc64_cpu --cores-on                # Get the number of cores currently online
ppc64_cpu --cores-on=X              # Put exactly X cores online

ppc64_cpu --dscr                    # Get current DSCR system setting
ppc64_cpu --dscr=<val>              # Change DSCR system setting
ppc64_cpu --dscr [-p <pid>]         # Get DSCR setting for process <pid>
ppc64_cpu --dscr=<val> [-p <pid>]   # Change DSCR setting for process <pid>

ppc64_cpu --smt-snooze-delay        # Get current smt-snooze-delay setting
ppc64_cpu --smt-snooze-delay=<val>  # Change smt-snooze-delay setting

ppc64_cpu --run-mode                # Get current diagnostics run mode
ppc64_cpu --run-mode=<val>          # Set current diagnostics run mode

ppc64_cpu --frequency [-t <time>]   # Determine cpu frequency for <time>
                                    # seconds, default is 1 second.

ppc64_cpu --subcores-per-core       # Get number of subcores per core
ppc64_cpu --subcores-per-core=X     # Set subcores per core to X (1 or 4)
ppc64_cpu --threads-per-core        # Get threads per core
ppc64_cpu --info                    # Display system state information)

```

The comparison scripts log the SMT state at the beginning of the
compression tests.

Currently the default on `p8.desy.de` is `smt==8` (and that status is
reset on reboot). This produces 160 processors if you check `lscpu`,
`/proc/cpuinfo`, `top`, `htop` or similar. With hyperthreading
disabled (`smt=off`) there are 20 processors.


### Number of threads

The tests performed until December 2016 show that the FPGA accelerator
can deliver compression rates approximately in the range [0.8, 1.1]
GByte/s with a single thread.

With multiple threads or processes approximately [1.6, 1.7] GB/s (half
for each when using two threads). This is in agreement with slide 11
of
[`CAPI_GENWQE-GZIP_for_DESY.pdf`](docs/CAPI_GENWQE-GZIP_for_DESY.pdf),
although slightly below the ideal performance, especially for XTC
files with a low compression ratio.

Two threads are enough to reach this performance in terms of
throughput, and adding more threads does not seem to produce any
increase in total throughput.


### Buffer size

The environment variables `ZLIB_IBUF_TOTAL` and `ZLIB_OBUF_TOTAL` can
be used to control the sizes of the compression buffers used by the
accelerator.  For low compresion ratio data throughput this option
does not seem to help much even for very large buffer sizes (compare
with slide 15 of
[`CAPI_GENWQE-GZIP_for_DESY.pdf`](docs/CAPI_GENWQE-GZIP_for_DESY.pdf).
The behavior with CAPI-enabled cards, for which this parameter seems
more relevant, remains to be tested.
