# Loading GDELT data into MongoDB

## GDELT 2.0 Encoding and Structure
The [GDELT](https://gdelt.org) dataset is a large dataset of news events that is updated
in real-time. GDELT stands for Global Database of Events Location and Tone. The format
of records in a GDELT data is defined by the [GDELT 2.0 Cookbook](http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf)

Each record uses an encoding method called CAMEO coding which is defined by the
[CAMEO cookbook](https://parusanalytics.com/eventdata/cameo.dir/CAMEO.Manual.1.1b3.pdf).

Once you understand the GDELT recording structure and the CAMEO encoding you will be able
to decode a record.

## How to download GDELT 2.0 data

The `gdeltloader/gdeltloader.py` script can download cameo data an unzip the files so that
they can be loaded into MongoDB.

```
$ python gdeltloader/gdeltloader.py -h
usage: gdeltloader.py [-h] [--host HOST] 
                        [--ziplist {master,incremental}] 
                        [--master MASTER] 
                        [--incremental INCREMENTAL] 
                        [--database DATABASE] 
                        [--collection COLLECTION] 
                        [--local LOCAL]
                        [--overwrite]
                        [--download] 
                        [--metadata]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           MongoDB URI [mongodb://localhost:27017]
  --ziplist {master,incremental}
                        Download master or incremental file
  --master MASTER       GDELT master file [http://data.gdeltproject.org/gdeltv2/masterfilelist.txt]
  --incremental INCREMENTAL
                        GDELT incremental file [http://data.gdeltproject.org/gdeltv2/lastupdate.txt]
  --database DATABASE   Default database for loading [GDELT]
  --collection COLLECTION
                        Default collection for loading [events_csv]
  --local LOCAL         load data from local list of zips
  --overwrite           Overwrite files when they exist already
  --download            download zip files from master or local file
  --metadata            grab meta data files
```

To operate first get the master list of event files.

``python gdeltloader/gdeltloader.py --ziplist master``

Now grab the subset of files you want. For us lets grab the last 365 days.
```shell
$ grep export gdelt_master-file-04-08-2019-14-13-28.txt | tail -n 365 > last_365_days.txt
$ wc last_365_days.txt
  365  1095 38847 last_365_days.txt
$
```

now download the data.

```shell
python gdeltloader/gdeltloader.py --host $MONGODB --download --local last_365_days.txt 
```

Now install pymongoimport

```sh
pipenv install pymongoimport
```

Now import the CSV files.
```
pymongoimport --host $MONGODB --fieldfile GDELT.ff --delimiter tab --database GDELT --collection events_csv *.CSV
```

You may also used [mongoimport](https://docs.mongodb.com/database-tools/mongoimport/) to load fields faster but remember to create a field file for that
program first. 

## transforming the data

You can generate GeoJSON points from the existing  geo-location lat/long filed
by using `gdeltloader/mapgeolocation.py`.

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
python gdeltloader/mapgeolocation.py
Processed documents total : 247441
```
If you run `mapgeolocation.py` on the same dataset it will overwrite the records.
Each new data-set will be merged into previous collections of documents. 



