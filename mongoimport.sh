#!/usr/bin/env sh
for i in *.CSV
do
  mongoimport --db=GDELT2 --collection=eventscsv  --type=tsv --fieldFile=gdelt_field_file.ff --mode=upsert --writeConcern "{w:1}" --columnsHaveTypes --file=$i $*
done
mongosh
