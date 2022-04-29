#!/usr/bin/env sh
cat *.export.CSV \
    | mongoimport \
        --collection=eventscsv \
        --mode=upsert \
        --writeConcern "{w:1}" \
        --type=tsv \
        --columnsHaveTypes \
        --fieldFile=gdelt_field_file.ff \
        $*
