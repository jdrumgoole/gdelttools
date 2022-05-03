"""
Importer for GDELT 2.0 raw data set.
https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/

The master file list is here:
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt

"""
import argparse
import sys
import os
import pymongo

from gdelttools.gdeltfile import download_gdelt_files, GDELTFilter
from gdelttools.gdeltwebdata import GDELTWebData
from gdelttools._version import __version__
from gdelttools.mongoimport import MongoImport


def main():

    parser = argparse.ArgumentParser(epilog=f"Version: {__version__}\n"
                                            f"More info : https://github.com/jdrumgoole/gdelttools ")

    parser.add_argument("--host",
                        help="MongoDB URI")

    parser.add_argument("--database", default="GDELT2",
                        help="Default database for loading [%(default)s]")

    parser.add_argument("--collection", default="eventscsv",
                        help="Default collection for loading [%(default)s]")
    parser.add_argument("--master",
                        default=False,
                        action="store_true",
                        help="GDELT master file [%(default)s]")

    parser.add_argument("--update",
                        default=False,
                        action="store_true",
                        help="GDELT update file [%(default)s]")

    parser.add_argument("--local", type=str,
                        help="load data from local list of zips")

    parser.add_argument("--overwrite",
                        default=False, action="store_true",
                        help="Overwrite files when they exist already")

    parser.add_argument("--download", default=False, action="store_true",
                        help="download zip files from master or local file")

    parser.add_argument("--importdata", default=False, action="store_true",
                        help="Import files into MongoDB")
    parser.add_argument("--metadata", action="store_true", default=False,
                        help="grab meta data files")

    parser.add_argument("--filter", default="all", type=GDELTFilter, choices=list(GDELTFilter),
                        help="download a subset of the data, the default is all data [export, mentions gkg, all]")

    parser.add_argument("--last", default=0, type=int, help="how many recent files to download default : [%(default)s] implies all files")

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    # if args.ziplist == "master":
    #     url = args.master
    # else:
    #     url = args.incremental



    try:
        # files_collection = None

        # if args.host:
        #     client = pymongo.MongoClient(host=args.host)
        #     db = client[args.database]
        #     files_collection = db["files"]
        #     events_collection = db[args.collection]

        if args.metadata:
            GDELTWebData.get_metadata()

        input_file_list = []

        if args.master:
            print(f"{GDELTWebData.master_url} ", end="")
            filename = GDELTWebData.get_master_list()
            print(f"-> {filename}")
            input_file_list.append(filename)

        if args.update:
            print(f"{GDELTWebData.update_url} ", end="")
            filename = GDELTWebData.get_update_list()
            print(f"-> {filename}")
            input_file_list.append(filename)

        if args.local:
            if os.path.isfile(args.local):
                input_file_list.append(args.local)
            else:
                print(f"'{args.local}' does not exist")
                sys.exit(1)

        if args.download:
            if len(input_file_list) > 0:
                csv_files = download_gdelt_files(input_file_list, args.last, args.filter, args.overwrite)
            else:
                print(f"No files listed for download")

        if args.importdata:
            importer = MongoImport(database_name=args.database, collection_name=args.collection)
            for f in csv_files:
                importer.import_data(f)

    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
