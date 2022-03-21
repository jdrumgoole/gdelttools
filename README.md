# gdeltloader
Scripts to load the GDELT data set into MongoDB

```
$ python gdeltloader/gdeltloader.py -h
usage: gdeltloader.py [-h] [--mongodb MONGODB]
                      [--ziplist {master,incremental}] [--master MASTER]
                      [--incremental INCREMENTAL] [--local LOCAL]
                      [--overwrite] [--download] [--mapgeo]

optional arguments:
  -h, --help            show this help message and exit
  --host URL            MongoDB URI [mongodb://localhost:27017]
  --ziplist {master,incremental}
                        Download master or incremental file
  --master MASTER       GDELT master file [http://data.gdeltproject.org/gdeltv
                        2/masterfilelist.txt]
  --incremental INCREMENTAL
                        GDELT incremental file
                        [http://data.gdeltproject.org/gdeltv2/lastupdate.txt]
  --local LOCAL         load data from local list of zips
  --overwrite           Overwrite files when they exist already
  --download            download zip files from master or local file
  --mapgeo              map all lat,lon data to GeoJSON
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
pymongoimport --host $MONGODB --fieldfile GDELT.ff --delimiter tab --database GDELT --collection events *.CSV
```

