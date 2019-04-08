# gdeltloader
Scripts to load the GDELT data set into MongoDB

```
$ python gdeltloader/gdeltloader.py  -h
usage: gdeltloader.py [-h] [--mongodb MONGODB]
                      [--download {master,incremental}] [--master MASTER]
                      [--incremental INCREMENTAL] [--local LOCAL]
                      [--overwrite] [--mapgeo]

optional arguments:
  -h, --help            show this help message and exit
  --mongodb MONGODB     MongoDB URI [mongodb://localhost:27017]
  --download {master,incremental}
                        Download master or incremental file
  --master MASTER       GDELT master file [http://data.gdeltproject.org/gdeltv
                        2/masterfilelist.txt]
  --incremental INCREMENTAL
                        GDELT incremental file
                        [http://data.gdeltproject.org/gdeltv2/lastupdate.txt]
  --local LOCAL         load data from local list of zips
  --overwrite           Overwrite files when they exist already
  --mapgeo              map all lat,lon data to GeoJSON
```
