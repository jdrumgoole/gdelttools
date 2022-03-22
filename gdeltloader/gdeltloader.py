"""
Importer for GDELT 2.0 raw data set.
https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/

The master file list is here:
http://data.gdeltproject.org/gdeltv2/masterfilelist.txt


"""
import argparse
import requests
import sys
from datetime import datetime
import os
import pymongo
import hashlib
import zipfile

from io import BytesIO
from zipfile import ZipFile
import urllib.request



def download_and_unzip(u: str):
    url_file = urllib.request.urlopen(u)

    with ZipFile(BytesIO(url_file.read())) as my_zip_file:
        my_zip_file.extractall()
        # for contained_file in my_zip_file.namelist():
        #     # with open(("unzipped_and_read_" + contained_file + ".file"), "wb") as output:
        #     for line in my_zip_file.open(contained_file).readlines():
        #         print(line)
        #         # output.write(line)


def compute_md5(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as input:
        buf = input.read()
        hasher.update(buf)

    return hasher.hexdigest()


def local_path(url):
    return url.split('/')[-1]


def download_file(url):
    local_filename = local_path(url)
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=8192), 1):
                if chunk:  # filter out keep-alive new chunks
                    print(".", end="")
                    if i % 80 == 0:
                        print("")
                    f.write(chunk)
                    # f.flush()
            if i % 80 != 0:
                print("")
    return local_filename


def extract_zip_file(filepath):
    zfile = zipfile.ZipFile(filepath)
    files = []
    for finfo in zfile.namelist():
        with zfile.open(finfo, "r") as input:
            with open(finfo, "w") as output:
                for i in input:
                    output.write(i.decode("utf-8"))
        files.append(finfo)

    return files


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--host", default="mongodb://localhost:27017",
                        help="MongoDB URI [%(default)s]")

    parser.add_argument("--ziplist", choices=["master", "incremental"],
                        default="incremental",
                        help="Download master or incremental file")

    parser.add_argument("--master",
                        default="http://data.gdeltproject.org/gdeltv2/masterfilelist.txt",
                        help="GDELT master file [%(default)s]")

    parser.add_argument("--incremental",
                        default="http://data.gdeltproject.org/gdeltv2/lastupdate.txt",
                        help="GDELT incremental file [%(default)s]")

    parser.add_argument("--database", default="GDELT",
                        help="Default database for loading [%(default)s]")

    parser.add_argument("--collection", default="events_csv",
                        help="Default collection for loading [%(default)s]")

    parser.add_argument("--local", help="load data from local list of zips")

    parser.add_argument("--overwrite",
                        default=False, action="store_true",
                        help="Overwrite files when they exist already")

    parser.add_argument("--download", default=False, action="store_true",
                        help="download zip files from master or local file")

    parser.add_argument("--metadata", action="store_true", default=False,
                        help="grab meta data files")
    args = parser.parse_args()

    if args.ziplist == "master":
        url = args.master
    else:
        url = args.incremental

    gdelt_md5_list = "http://data.gdeltproject.org/events/md5sums"
    gdelt_file_sizes = "http://data.gdeltproject.org/events/filesizes"

    client = pymongo.MongoClient(host=args.host)
    db = client[args.database]
    files_collection = db["files"]
    events__collection = db[args.collection]

    if args.metadata:
        r = requests.get(gdelt_md5_list, allow_redirects=True)
        with open("gdelt_md5sums", "w") as output_file:
            output_file.write(r.content.decode("utf-8"))
        print(f"downloaded {gdelt_md5_list} to gdelt_md5sums")
        r = requests.get(gdelt_file_sizes, allow_redirects=True)
        with open("gdelt_filesizes", "w") as output_file:
            output_file.write(r.content.decode("utf-8"))
        print(f"downloaded {gdelt_file_sizes} to gdelt_filesizes")

    if args.local:
        if os.path.isfile(args.local):
            filename = args.local
        else:
            print(f"'{args.local}' does not exist")
            sys.exit(1)
    elif args.ziplist:
        if args.ziplist == "master":
            print(f"Getting incremental file from '{url}'")
            url = args.master
        else:
            print(f"Getting master file from '{url}'")
            url = args.incremental

        r = requests.get(url, allow_redirects=True)

        filename = f"gdelt_{args.ziplist}-file-{datetime.utcnow().strftime('%m-%d-%Y-%H-%M-%S')}.txt"
        print(f"Creating local master file: '{filename}'")
        open(filename, 'w').write(r.content.decode("utf-8"))

    if args.download:
        with open(filename, "r") as file_list:
            for l in file_list:
                size, md5, zip = l.split()
                size = int(size)
                md5 = str(md5)
                # print(f"{size}:{sha}:{zip}")
                if os.path.exists(local_path(zip)) and not args.overwrite:
                    print(f"File '{local_path(zip)}'exists locally")
                    local_zip_file = local_path(zip)
                else:
                    print(f"Downloading:'{zip}'")
                    print(f"size:{size}")
                    print(f"md5:{md5}")
                    local_zip_file = download_file(zip)
                    print(f"created: '{local_zip_file}'")

                    computed_md5 = compute_md5(local_zip_file)
                    if computed_md5 == md5:
                        files_collection.insert_one({"ts": datetime.utcnow(),
                                                     "remote": zip,
                                                     "local": local_zip_file,
                                                     "size": size,
                                                     "md5": md5})
                    else:
                        print(
                            f"'{md5}' checksum for doesn't match computed checksum: {computed_md5} for {local_zip_file}")
                        continue

                print(f"Unzipping: '{local_zip_file}'")

                local_csv_files = extract_zip_file(local_zip_file)

                for i in local_csv_files:
                    print(l)
