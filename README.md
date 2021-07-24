# GPX to CSV conversion (or to a Python list)

This tool can convert most gpx files to csv format. It preserves trackpoint extensions and `trk` level tags. It should support multiple `<trk>` entries per file, multiple `<trkseg>` segments. `trk` and `trkseg` specific tags should be added as columns to the final csv file distinguishing the different tracks from each other. 

The module uses the GPX tags as column names. It should be able to process any gpx file, not just ones with specific data. If a gpx file uses extensions and has `hr` for heartrate data, it will make a csv with a `hr` column.

However, column names will simply reflect how they are tagged in the gpx file. Column ordering may be suboptimal, currently I'm simply sorting it alphabetically, so latitude and longitude may not be adajacent.

Requires `lxml` and python 3.6+


## Usage

1. Clone and install module (pip install coming soon)
```python
git clone https://github.com/astrowonk/gpxcsv.git
cd gpxcsv
python setup.py install
```
2. Use directly with command line tool or as a python module. The following examples will create `input.csv`
```
gpxcsv input.gpx
python -m input.gpx
```
Or specify an output file name
```
gpxcsv input.gpx -o new_name.csv
```
3. Use the `gpxtolist` function to read the gpx file into a python list suitable for conversion into a pandas dataframe in a notebook or ipython.

```
from gpxcsv import gpxtolist
gpx_list = gpxcsv('myfile.gpx')

#if you have pandas
import pandas as pd
df = pd.DataFrame(gpx_list)

```

## Test CSV files

I tested the conversion against a handful of my own GPX files (exported from Apple Health / Apple Watch via the excellent [HealthFit app](https://apps.apple.com/us/app/healthfit/id1202650514)).

In addition I used several files from this [sample-gpx repository](https://github.com/gps-touring/sample-gpx), specifically:

* bogus_basin.gpx
* Alt_Portsmouth.gpx
* MoselradwegAusWiki.gpx
* VoieVerteHauteVosges.gpx

as well as all the test files from [gpxpy](https://github.com/tkrajina/gpxpy/tree/dev/test_files). Many of those intentionally lack any coherent flow of `trk -> trkseg -> trkpt` so they don't produce a valid csv file.

The __bogus_basin__ file is a good example of conversion of multiple `trk` files. Though, the design case was more a single workout tracked with an Apple Watch (as that's the data I'm interested in myself.)

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

