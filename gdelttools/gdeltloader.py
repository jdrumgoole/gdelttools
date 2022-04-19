"""
Importer for GDELT 2.0 raw data set.
https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/

The master file list is here:
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt

"""
import argparse
from typing import List

import requests
import sys
from datetime import datetime
import os
import pymongo

from gdelttools.web import local_path, download_file, compute_md5, extract_zip_file
from gdelttools.gdeltcsv import Downloader


def download_zips(collection, file_list: List[str]):
    for f in file_list:
        with open(f, "r") as input_file:
            for line in input_file:
                size, md5, zipurl = line.split()
                size = int(size)
                md5 = str(md5)
                # print(f"{size}:{sha}:{zip}")
                local_zip_file = local_path(zipurl)
                if os.path.exists(local_zip_file) and not args.overwrite:
                    print(f"File '{local_zip_file}'exists locally cannot overwrite")
                    sys.exit(1)
                else:
                    print(f"Downloading:'{zipurl} size: {size}'")
                    download_file(zipurl)
                    computed_md5 = compute_md5(local_zip_file)

                if computed_md5 == md5:
                    print(f"Unzipping: '{local_zip_file}'")
                    local_csv_files = extract_zip_file(local_zip_file)
                    if collection:
                        collection.insert_one({"_id": zipurl,
                                               "ts": datetime.utcnow(),
                                               "local_zip_file": local_zip_file,
                                               "local_csv_file": local_csv_files[0],
                                               "size": size,
                                               "md5_zip_file": md5})
                else:
                    print(f"'{md5}' checksum for {zip} doesn't match computed\n"
                          f" checksum: {computed_md5} for {local_zip_file}")
                    sys.exit(0)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--host",
                        help="MongoDB URI")

    parser.add_argument("--master",
                        default=False,
                        action="store_true",
                        help="GDELT master file [%(default)s]")

    parser.add_argument("--update",
                        default=False,
                        action="store_true",
                        help="GDELT update file [%(default)s]")

    parser.add_argument("--database", default="GDELT",
                        help="Default database for loading [%(default)s]")

    parser.add_argument("--collection", default="events_csv",
                        help="Default collection for loading [%(default)s]")

    parser.add_argument("--local", type=str,
                        help="load data from local list of zips")

    parser.add_argument("--overwrite",
                        default=False, action="store_true",
                        help="Overwrite files when they exist already")

    parser.add_argument("--download", default=False, action="store_true",
                        help="download zip files from master or local file")

    parser.add_argument("--metadata", action="store_true", default=False,
                        help="grab meta data files")
    args = parser.parse_args()

    # if args.ziplist == "master":
    #     url = args.master
    # else:
    #     url = args.incremental

    gdelt_md5_list = "http://data.gdeltproject.org/events/md5sums"
    gdelt_file_sizes = "http://data.gdeltproject.org/events/filesizes"

    files_collection = None
    if args.host:
        client = pymongo.MongoClient(host=args.host)
        db = client[args.database]
        files_collection = db["files"]
        events_collection = db[args.collection]

    if args.metadata:
        Downloader.get_metadata()

    input_file_list = []
    if args.local:
        if os.path.isfile(args.local):
            input_file_list.append(args.local)
        else:
            print(f"'{args.local}' does not exist")
            sys.exit(1)
    elif args.master or args.update:
        if args.update:
            print(f"Getting update file from '{Downloader.update_url}'")
            filename = Downloader.get_update_list()
            input_file_list.append(filename)
            print(f"created: {filename}")
        if args.master:
            print(f"Getting master file from '{Downloader.master_url}'")
            filename = Downloader.get_master_list()
            print(f"created: {filename}")
            input_file_list.append(filename)

    if args.download:
        download_zips(files_collection, input_file_list)


if __name__ == "__main__":
    main()
