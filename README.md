# GPX to CSV conversion (or to a Python list)

[![Downloads](https://static.pepy.tech/personalized-badge/gpxcsv?period=total&units=international_system&left_color=lightgrey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/gpxcsv)

[PyPi Project Page](https://pypi.org/project/gpxcsv/) 

This tool can convert most gpx files to csv format. It preserves trackpoint extensions and `trk` level tags. It supports multiple `<trk>` entries per file, multiple `<trkseg>` segments. It powers [gpxrun](https://github.com/astrowonk/gpxrun) and [my gpx analysis web app](https://marcoshuerta.com/gpxrun/).

## Advantages / Features

* **Preserves most trackpoint data:** If a gpx file uses extensions and has `hr` for heartrate data, it will make a csv with a `hr` column. No need to ever add specific support for specific new or requested column names.

* **Minimal dependencies:** Only requires lxml.

* **Easy command line usage with wildcards:** `gpxcsv file.gpx` and done. `gpxcsv *.gpx` just works.

* **Preserves and identifies multi-trk or multi-trkseg data:** Because `trk` and `trkseg` level tags get their own ID columns, multi-track or segment files preserve each segment or track as distinguishable.

* **Easily create Pandas dataframe:** The `gpxtolist` function will create a python list for one-line conversation to a dataframe: `pd.DataFrame(gpxtolist('myfile.gpx'))`

* **Supports JSON (even though I named the package gpxcsv):** JSON support since it was easy from the list of dictionaries.


## Installation and Usage

1. Pip install
```python
pip install gpxcsv
```

Or clone and install module
```python
git clone https://github.com/astrowonk/gpxcsv.git
cd gpxcsv
python setup.py install
```
2. Use directly with command line tool or as a python module. The following examples will create `myrun.csv`
```
gpxcsv myrun.gpx
python -m gpxcsv myrun.gpx
```
Or specify an output file name
```
gpxcsv myrun.gpx -o myfirstrun.csv
```

Or, even though I named this gpxcsv, convert to a simple json file:

```python
gpxcsv myrun.gpx --json
python -m gpxcsv myrun.gpx -j
python myrun.gpx -o out.json
```

3. Use the `gpxtolist` function to read the gpx file into a python list suitable for conversion into a pandas dataframe in a notebook or iPython.

```
from gpxcsv import gpxtolist
gpx_list = gpxtolist('myfile.gpx')

#if you have pandas
import pandas as pd
df = pd.DataFrame(gpx_list)

```

## Release Notes


### 0.2.15

* Fixes issue with `trk` level extension data like `DisplayColor`. This will now be added to the csv file with an identifier along with `trk` name.

### 0.2.14

* Fixes issue with gpx files that don't have children of the extension, i.e. no `TrackPointExtension` inside the `Extensions` tag.
### 0.2.11

* Adds support for processing a `StringIo` object, which was necessary to use this code as the backend for a Dash web app, which encodes all files as base64 strings.

### 0.2.10

* The _try_to_float function no longer crashes when trying to floatify None. This was happening due to some odd xml in Runalyze exported GPX files.
### 0.2.9

* Changed the way attribs are pulled from trackpoints. Code will not crash if trackpoint is missing lat or lon. (Obviously this shouldn't happen, but occurs in some exported workouts from Apple Watch that are missing GPS data.)

### 0.2.8

* Fixed a crashing bug because of an unneccessary import accidentally auto-added.

* Added 0.2.7 fixes, which includes the --silent flag and better handling of missing files (skipping processing them rather than an assert error)



## Test GPX files

I tested the conversion against a handful of my own GPX files (exported from Apple Health / Apple Watch via the excellent [HealthFit app](https://apps.apple.com/us/app/healthfit/id1202650514)).

In addition I used several files from this [sample-gpx repository](https://github.com/gps-touring/sample-gpx), specifically:

* Alt_Portsmouth.gpx
* MoselradwegAusWiki.gpx
* VoieVerteHauteVosges.gpx

as well as all the test files from [gpxpy](https://github.com/tkrajina/gpxpy/tree/dev/test_files). Many of those intentionally lack any coherent flow of `trk -> trkseg -> trkpt` so they don't produce a valid csv file.

I also used a __bogus_basin__ file ([src](https://raw.githubusercontent.com/FrancescoRigoni/Android_GPX_SampleProject/master/app/src/main/assets/bogus_basin.gpx)) which is a good example of conversion of multiple `trk` files. Though, the design case was more a single workout tracked with an Apple Watch (as that's the data I'm interested in myself.)

## Example Input and Output:

Here the beginning of a `tkpt` from a HealthFit/Apple HealthKit tracked run, with gps coords altered.

```
<trk>
<type>running</type>
<trkseg>
<trkpt lat="45.0000" lon="-75.0000">
    <ele>51.0000</ele>
    <time>2021-07-21T12:37:41.000Z</time>
    <extensions>
        <gpxtpx:TrackPointExtension>
            <gpxtpx:atemp>24</gpxtpx:atemp>
            <gpxtpx:cad>72</gpxtpx:cad>
            <gpxtpx:speed>2.147612</gpxtpx:speed>
            <gpxtpx:hAcc>6.406485</gpxtpx:hAcc>
            <gpxtpx:vAcc>5.718293</gpxtpx:vAcc>
        </gpxtpx:TrackPointExtension>
    </extensions>
...
```

This produces a CSV that begins:

```
atemp,cad,course,ele,hAcc,hr,lat,lon,speed,time,type,vAcc
24.0,72.0,,51.0,6.406485,,45.0,-75.0,2.147612,2021-07-21T12:37:41.000Z,running,5.718293
```

Note that the `hr` column is not in the first trackpoint (or first several) but the header appears in the csv file.
