
# Other compression tools/algorithms (software implementations).

## Summary

Here we look into the performance of the
[lz4](https://github.com/lz4/lz4) for some of the crystallography raw
data files from the [Coherent X-ray Imaging Data Bank,
CXIDB](http://cxidb.org).

In some cases lz4 would be able to deliver good compression ratios at
rates of the order of several hundreds of MB/s, see for example
[benchmarks table from its
README](https://github.com/lz4/lz4#benchmarks).

## Quick comparison

This outlines a very quick comparison with easily-compressible HDF5
files on a virtual machine (osboxes Ubuntu 16.04) running on an XFEL
Windows host machine:

These tests use default compression levels (6 for gzip, and 1=fast for
lz4).

### MC0027 file, with compression ratio of up to 25-50.

```
osboxes@osboxes:~$ ls -la MC0027-T0000-e500-*
-rw-r--r-- 1 osboxes osboxes  101848738 Nov 23 11:31 MC0027-T0000-e500-c=16k2-hw.h5
-rw-r--r-- 1 osboxes osboxes 2595571800 Nov 25 09:28 MC0027-T0000-e500-no-comp.h5
-rw-rw-r-- 1 osboxes osboxes   40473056 Nov 25 09:39 MC0027-T0000-e500-no-comp.h5.gz
-rw-rw-r-- 1 osboxes osboxes   78953224 Nov 25 09:38 MC0027-T0000-e500-no-comp.h5.z4
```

lz4 seems to:

* Be able to compress more than FPGA-DEFLATE at a rate of >400MB/s:

```
osboxes@osboxes:~$ /usr/bin/time -f '%e %U %S' lz4 -f MC0027-T0000-e500-no-comp.h5 MC0027-T0000-e500-no-comp.h5.z4
Compressed 2595571800 bytes into 78953224 bytes ==> 3.04%                      
5.90 1.37 1.38

```
(approx 419.5 MB/s)


* Run ~5.6 times faster than gzip:

```
/usr/bin/time -f '%e %U %S' gzip < MC0027-T0000-e500-no-comp.h5 > MC0027-T0000-e500-no-comp.h5.gz
33.26 29.54 2.86
```
(approx 74.4 MB/s)


### MC0017-T0000-e500-no-comp.h5

For this file the compresion ratio ranges between approximately 8.6
(lz4), 11.6 (FPGA DEFLATE), and 17.5 (software gzip with default (6)
compression level).



```
osboxes@osboxes:~$ ls -la MC0017-T0000-*
-rw-r--r-- 1 osboxes osboxes  381076100 Nov 25 09:21 MC0017-T0000-e500-hw-comp.h5
-rw-r--r-- 1 osboxes osboxes 4438783240 Nov 25 09:27 MC0017-T0000-e500-no-comp.h5
-rw-rw-r-- 1 osboxes osboxes  253515102 Nov 25 10:08 MC0017-T0000-e500-no-comp.h5.gz
-rw-rw-r-- 1 osboxes osboxes  515964504 Nov 25 10:11 MC0017-T0000-e500-no-comp.h5.z4
```

With this file the results for lz4. are not as impressive as with
`MC0027`.

* lz4 compresses less than FGPA-DEFLATE (and software gzip):

```
osboxes@osboxes:~$ /usr/bin/time -f '%e %U %S' lz4 -f MC0017-T0000-e500-no-comp.h5 MC0017-T0000-e500-no-comp.h5.z4
Compressed 4438783240 bytes into 515964504 bytes ==> 11.62%                    
51.54 4.84 1.51
```

(approx 82.1 MB/s)


With gzip:

```
osboxes@osboxes:~$ /usr/bin/time -f '%e %U %S' gzip < MC0017-T0000-e500-no-comp.h5 > MC0017-T0000-e500-no-comp.h5.gz
138.28 114.49 12.70
```

(approx 30.6 MB/s)
