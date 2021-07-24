# GPX to CSV conversion (or to a python list)

This tool can convert most gpx files to csv format. It preserves trackpoint extensions and `trk` level tags. It should support multiple `<trk>` entries per file, multiple `<trkseg>` segments.

`gpxcsv` uses the GPX tags as column names. It should be able to process any gpx file, not just ones with specific data nor will it ignore any fields. However, column names may be a bit ambigious as it will not give them any meaningful column names beyond what is in the gpx data. And column ordering may be suboptimal, given the code has no preconceived notions of what columns will be there - latitude and longitude may not be adajacent for example.

Requires `lxml` and python 3.6+ (I like having f-strings)


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
