"""
Importer for GDELT 2.0 raw data set.
https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/

The master file list is here:
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt

"""
import argparse
from typing import List

from requests import exceptions
import sys
from datetime import datetime
import os
import pymongo

from gdelttools.web import local_path, download_file, compute_md5, extract_zip_file
from gdelttools.gdeltcsv import Downloader
from gdelttools._version import __version__


def download_zips(collection, file_list: List[str], last=None, file_filter=None, overwrite=False):
    if file_filter == None:
        file_filter = "export"
    if last is None or last < 0:
        last = 0

    for f in file_list:
        lines = []
        with open(f, "r") as input_file:
            for input_line in input_file:
                lines.append(input_line)

            if last > 0 :
                section = len(lines) - (last * 3)  # three files per set, gkg, exports, mentions
                lines = lines[section:]  # slice the last days

            for l in lines:
                try:
                    size, md5, zipurl = l.split()
                    size = int(size)
                    md5 = str(md5)
                    # print(f"{size}:{sha}:{zip}")
                    if (file_filter in zipurl) or (file_filter == "all"):
                        local_zip_file = local_path(zipurl)
                        if os.path.exists(local_zip_file) and not overwrite:
                            print(f"File '{local_zip_file}'exists already")
                        else:
                            download_file(zipurl)

                        computed_md5 = compute_md5(local_zip_file)

                        if computed_md5 == md5:

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
                except exceptions.HTTPError as e:
                    print(f"Error for {zipurl}")
                    print(e)


def main():

    parser = argparse.ArgumentParser(epilog=f"Version: {__version__}\n"
                                            f"More info : https://github.com/jdrumgoole/gdelttools ")

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

    parser.add_argument("--filefilter", default="export", choices=["export", "gkg", "mentions", "all"],
                        help="download a subset of the data, the default is the export data")

    parser.add_argument("--last", default=0, type=int, help="how many recent days of data to download default : [%(default)s] implies all files")

    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')
    args = parser.parse_args()

    # if args.ziplist == "master":
    #     url = args.master
    # else:
    #     url = args.incremental

    gdelt_md5_list = "http://data.gdeltproject.org/events/md5sums"
    gdelt_file_sizes = "http://data.gdeltproject.org/events/filesizes"

    try:
        files_collection = None

        if args.host:
            client = pymongo.MongoClient(host=args.host)
            db = client[args.database]
            files_collection = db["files"]
            events_collection = db[args.collection]

        if args.metadata:
            Downloader.get_metadata()

        input_file_list = []

        if args.master:
            filename = Downloader.get_master_list(args.overwrite)
            input_file_list.append(filename)

        if args.update:
            filename = Downloader.get_update_list(args.overwrite)
            input_file_list.append(filename)

        if args.local:
            if os.path.isfile(args.local):
                input_file_list.append(args.local)
            else:
                print(f"'{args.local}' does not exist")
                sys.exit(1)

        if args.download:
            if len(input_file_list) > 0:
                download_zips(files_collection, input_file_list, args.last, args.filefilter, args.overwrite)
            else:
                print(f"No files listed for download")
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
