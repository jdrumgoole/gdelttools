#!/usr/bin/env sh
# Upload all the CSV files in your current directory to a MongoDB cluster.
#
# Any parameters passed to this command are passed to mongoimport, so to
# connect to your cluster, provide the --uri parameter with your MongoDB
# connection string, like this:
# 
# ./mongoimport.sh --uri "mongodb+srv://<username>:<password>@abcde.mongodb.com/<yourdatabase>"


cat *.export.CSV \
    | mongoimport \
        --collection=eventscsv \
        --mode=upsert \
        --writeConcern "{w:1}" \
        --type=tsv \
        --columnsHaveTypes \
        --fieldFile=gdelt_field_file.ff \
        $*
