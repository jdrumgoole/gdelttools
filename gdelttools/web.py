import hashlib
import urllib
import zipfile
import requests
from requests import exceptions
from io import BytesIO
import os



def download_and_unzip(u: str):
    url_file = urllib.request.urlopen(u)

    with zipfile.ZipFile(BytesIO(url_file.read())) as my_zip_file:
        my_zip_file.extractall()


def compute_md5(file):
    hasher = hashlib.md5()
    with open(file, 'rb') as input:
        buf = input.read()
        hasher.update(buf)

    return hasher.hexdigest()


def local_path(url):
    filename_with_args = url.split('/')[-1]
    filename = filename_with_args.split('?')[0]
    return filename


def download_file(url, overwrite=False):
    local_filename = local_path(url)
    # NOTE the stream=True parameter below

    if os.path.exists(local_filename) and not overwrite:
        print(f"{local_filename} already exists")
        return local_filename
    else:
        print(f"Downloading: {url}")

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for i, chunk in enumerate(r.iter_content(chunk_size=8192), 1):
                width = os.get_terminal_size().columns
                if chunk:  # filter out keep-alive new chunks
                    print(".", end="")
                    if i % width == 0:
                        print("")
                    f.write(chunk)
                    # f.flush()
            if i % width != 0:
                print("")

    return local_filename


def extract_zip_file(filepath):
    files = []
    with zipfile.ZipFile(filepath) as archive:
        print(f"unzipping: '{filepath}'")
        for zfilename in archive.namelist():
            if os.path.exists(zfilename):
                print(f"{zfilename} exists, skipping unzipping")
                continue
            text = archive.read(zfilename).decode(encoding="utf-8")
            print(f"extracting: '{zfilename}'")
            with open(zfilename, "w") as output_file:
                output_file.write(text)
            files.append(zfilename)

    return files
