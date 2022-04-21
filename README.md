## Loading GDELT data into MongoDB

This is a set of programs for loading the [GDELT 2.0](https:/gdeltproject.org) data set into MongoDB. 

## Quick Start

Install the latest version of Python from [python.org](https://www.python.org/downloads/)
You need at least version 3.6 for this program. Many versions of Python that
come pre-installed are only 2.7. This version will not work.

Now install `gdelttools`

```shell
pip install gdelttools
```

Now get the master file of all the GDELT files. 

```shell
gdeltloader --master
```

This will generate a file named something like `gdelt-master-file-04-19-2022-19-33-56.txt`

## Downloading the master data set

To download the master data set associated with GDELT (the export files) you can combine
these steps:

```shell
gdeltloader --master --download --overwrite
```

This will get the master file, parse it, extract the list of CSV files and unzip them.
the full GDELT 2.0 database runs to several terabytes of data so this is not recommend. 

To limit the amount you download you can specify `--last` to define how many days of data
you want to download:

```shell
gdeltloader --master --download --overwrite --last 20
```
Will download the most recent 20 days of data. 

### GDELT 2.0 Encoding and Structure
The [GDELT](https://gdeltproject.org) dataset is a large dataset of news events that is updated
in real-time. GDELT stands for Global Database of Events Location and Tone. The format
of records in a GDELT data is defined by the [GDELT 2.0 Cookbook](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)

Each record uses an encoding method called CAMEO coding which is defined by the
[CAMEO cookbook](https://parusanalytics.com/eventdata/cameo.dir/CAMEO.Manual.1.1b3.pdf).

Once you understand the GDELT recording structure and the CAMEO encoding you will be able
to decode a record. To fully decode a record you may need the 
[TABARI](https://github.com/openeventdata/tabari_dictionaries) dictionaries
from which the CAMEO encoding is derived. 

## How to download GDELT 2.0 data

The `gdeltloader` script can download cameo data an unzip the files so that
they can be loaded into MongoDB.

```
usage: gdeltloader [-h] [--host HOST] [--master] [--update]
                   [--database DATABASE] [--collection COLLECTION]
                   [--local LOCAL] [--overwrite] [--download] [--metadata]
                   [--filefilter {export,gkg,mentions,all}] [--last LAST]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           MongoDB URI
  --master              GDELT master file [False]
  --update              GDELT update file [False]
  --database DATABASE   Default database for loading [GDELT]
  --collection COLLECTION
                        Default collection for loading [events_csv]
  --local LOCAL         load data from local list of zips
  --overwrite           Overwrite files when they exist already
  --download            download zip files from master or local file
  --metadata            grab meta data files
  --filefilter {export,gkg,mentions,all}
                        download a subset of the data, the default is the
                        export data
  --last LAST           how many recent days of data to download [365]

Version: 0.06a
```

Here is how to download the last 365 days of GDELT data. 

```
gdeltloader --master --update --download --last 365``
````
This command will only download the `export` files for the last 365 days which
are the files we are interested in. 

## How to import downloaded data into MongoDB

Now import the CSV files with [mongoimport](https://docs.mongodb.com/database-tools/mongoimport/).

There is a [mongoimport.sh](https://raw.githubusercontent.com/jdrumgoole/gdelttools/master/mongoimport.sh)
script in the [gdelttools](https://github.com/jdrumgoole/gdelttools) repo
which is already configured with the right arguments.  There is also a corresponding
field file, 
[gdelt_field_file.ff](https://raw.githubusercontent.com/jdrumgoole/gdelttools/master/gdelt_field_file.ff) 
which this script uses to ensure correct type mappings.

To run:

`sh mongoimport.sh`

it will upload all the CSV files in the current working directory. 

### transforming the data

With our data now in MongoDB, we have some cleanup to do. 
The next steps refine and reshape the data via Aggregation Pipelines. 
To run these aggregations, I used the 
[MongoDB Extension for VSCode](https://code.visualstudio.com/docs). 
Just connect to your cluster, then run the aggregations in this repo (in order!).

1. Convert raw latitude, longitude strings to double type. Then, create GeoJSON points out of them. You can do this by running the `convert-geojson-pipeline.mongodb` aggregation. 

2. Compress the documents. You can do this by running the `compress-pipeline.mongodb` aggregation.


You can generate GeoJSON points from the existing  geo-location lat/long filed
by using `gdelttools/mapgeolocation.py`.

```shell
usage: mapgeolocation.py [-h] [--host HOST] [--database DATABASE] [-i INPUTCOLLECTION] [-o OUTPUTCOLLECTION]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           MongoDB URI [mongodb://localhost:27017]
  --database DATABASE   Default database for loading [GDELT]
  -i INPUTCOLLECTION, --inputcollection INPUTCOLLECTION
                        Default collection for input [events_csv]
  -o OUTPUTCOLLECTION, --outputcollection OUTPUTCOLLECTION
                        Default collection for output [events]
```
This program expects to read and write data from a database called GDELT. The 
default input collection is `events_csv` and the default output collection is 
`events`.

To transform the collections run:
```shell
python gdelttools/mapgeolocation.py
Processed documents total : 247441
```
If you run `mapgeolocation.py` on the same dataset it will overwrite the records.
Each new data-set will be merged into previous collections of documents. 



