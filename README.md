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
  --ziplist {master,incremental}
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
python  --mongodb mongodb+srv://<username:<password>@gdelt-rgl39.mongodb.net/test?retryWrites=true --download last_365_days.txt 
```

Now install pymongo_import

```sh
pipenv install pymongo_import
```

pymongo_import --host $MONGODB --fieldfile GDELT.ff --delimiter tab --database GDELT --collection events *.CSV

Partial index - didn't work
db.events_geo.createIndex( { "Actor1Geo" : "2dsphere"}, {partialFilterExpression: {"Actor1Geo.coordinates.0": {$type: "number"}, "Actor1Geo.coordinates.1": {$type: "number"} }})
db.events_geo.createIndex( { "Actor2Geo" : "2dsphere"}, {partialFilterExpression: {"Actor2Geo.coordinates.0": {$type: "number"}, "Actor2Geo.coordinates.1": {$type: "number"} }})
db.events_geo.createIndex( { "ActionGeo" : "2dsphere"}, {partialFilterExpression: {"ActionGeo.coordinates.0": {$type: "number"}, "ActionGeo.coordinates.1": {$type: "number"} }})

db.events_stripped.find(
   {
     ActionGeo:
       { '$geoNear' :
          {
            '$geometry': { type: "Point",  coordinates: [ -0.118092, 51.509865 ] },
            '$minDistance': 1000,
            '$maxDistance': 5000
          }
       }
   }
)

db.events.aggregate( [
   {
     "$project" : {
         "ActionGeo": {
            $cond: {
               if: { $eq: [ "", "$ActionGeo.coordinates.0" ] },
               then: "$$REMOVE",
               else: "ActionGeo.coordinates.0"
            }
         }
      }
   }
] )

===>
MongoDB Enterprise GDELT-shard-0:PRIMARY> cond1
{
	"$cond" : {
		"if" : {
			"$eq" : [
				"$Actor1Geo_Long",
				""
			]
		},
		"then" : 0,
		"else" : "$Actor1Geo_Long"
	}
}

MongoDB Enterprise GDELT-shard-0:PRIMARY> cond2
{
	"$cond" : {
		"if" : {
			"$eq" : [
				"$Actor1Geo_Lat",
				""
			]
		},
		"then" : 0,
		"else" : "$Actor1Geo_Lat"
	}
}
MongoDB Enterprise GDELT-shard-0:PRIMARY>

MongoDB Enterprise GDELT-shard-0:PRIMARY> adder
{
	"$addFields" : {
		"ActionGeo" : {
			"type" : "Point",
			"coordinates" : [
				{
					"$cond" : {
						"if" : {
							"$eq" : [
								"$Actor1Geo_Long",
								""
							]
						},
						"then" : 0,
						"else" : "$Actor1Geo_Long"
					}
				},
				{
					"$cond" : {
						"if" : {
							"$eq" : [
								"$Actor1Geo_Lat",
								""
							]
						},
						"then" : 0,
						"else" : "$Actor1Geo_Lat"
					}
				}
			]
		}
	}
}
