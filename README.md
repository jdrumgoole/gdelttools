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

Now using the file you just generated run this `grep` 
command to extract the last 365 days of data. Note you will need to
substitute the file you just created. 

```shell
grep export gdelt-master-file-[MM-DD-YYYY-HH-MM-SS].txt | tail -n 365 > last_365_days.txt  | tail -n 365 > last_365_days.txt
```

Now you can download the list of files you just created using the command

```shell
gdeltloader --download --local last_365_days.txt
```

### GDELT 2.0 Encoding and Structure
The [GDELT](https://gdelt.org) dataset is a large dataset of news events that is updated
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
```

To operate first get the master and the update list of event files.

``gdeltloader --master --update``

Now grab the subset of files you want. For us lets grab the last 365 days of events. There 
are three times of files in the master and update files:
```
150383 297a16b493de7cf6ca809a7cc31d0b93 http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip
318084 bb27f78ba45f69a17ea6ed7755e9f8ff http://data.gdeltproject.org/gdeltv2/20150218230000.mentions.CSV.zip
10768507 ea8dde0beb0ba98810a92db068c0ce99 http://data.gdeltproject.org/gdeltv2/20150218230000.gkg.csv.zip
```

Export files contain event data. Mentions contain other mentions of the initial news event in the current 15
minute cycle. GKS files contain the global knowledge graph.

We just want the previous 365 days of events so we use the master file to get the previous 
365 exports files as so. 

```shell
$ grep export gdelt_master-file-04-08-2019-14-13-28.txt | tail -n 365 > last_365_days.txt
$ wc last_365_days.txt
  365  1095 38847 last_365_days.txt
$
```

now download the data.

```shell
gdeltloader --download --local last_365_days.txt 
```

Host tells us a database to store the files we have downloaded. The local argument tells us
the location of the local file on disk. This command will download all the associated zip files
and unpack them into uncompress .CSV files. 


Now import the CSV files with [mongoimport](https://docs.mongodb.com/database-tools/mongoimport/).

**Need mongoimport example here**

### transforming the data

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



