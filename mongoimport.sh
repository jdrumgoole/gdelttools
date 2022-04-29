#!/usr/bin/env sh
# Upload all the CSV files in your current directory to a MongoDB cluster.
#
# Any parameters passed to this command are passed to mongoimport, so to
# connect to your cluster, provide the --uri parameter with your MongoDB
# connection string, like this:
# 
# ./mongoimport.sh --uri "mongodb+srv://<username>:<password>@abcde.mongodb.com/<yourdatabase>"

findme() {
    # Function for finding the path of a shell script,
    # taken from https://stackoverflow.com/a/246128
    TARGET_FILE=$0

    cd `dirname $TARGET_FILE`
    TARGET_FILE=`basename $TARGET_FILE`

    # Iterate down a (possible) chain of symlinks
    while [ -L "$TARGET_FILE" ]
    do
        TARGET_FILE=`readlink $TARGET_FILE`
        cd `dirname $TARGET_FILE`
        TARGET_FILE=`basename $TARGET_FILE`
    done

    # Compute the canonicalized name by finding the physical path 
    # for the directory we're in and appending the target file.
    PHYS_DIR=`pwd -P`
    RESULT=$PHYS_DIR/$TARGET_FILE
    echo $RESULT
}

myloc=$(dirname $(findme $0))

fieldfile="${myloc}/gdelt_field_file.ff"

cat *.export.CSV \
    | mongoimport \
        --collection=eventscsv \
        --mode=upsert \
        --writeConcern '{w:1}' \
        --type=tsv \
        --columnsHaveTypes \
        --fieldFile="${fieldfile}" \
        $*
