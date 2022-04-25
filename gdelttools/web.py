import hashlib
import urllib
import zipfile
import requests
from requests import exceptions
from typing import List
from io import BytesIO
import os
from enum import Enum
import sys
import zipfile
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


def skip_this_file(zip_filename: str, overwrite: bool = None):
    name, ext = os.path.splitext(zip_filename)
    csv_filename = f"{name}.CSV"
    if overwrite:
        return overwrite
    else:
        name, ext = os.path.splitext(zip_filename)
        csv_filename = f"{name}.CSV"
        return os.path.exists(zip_filename) or os.path.exists(csv_filename)


class WebDownload:

    CHUNK_SIZE = 1024 * 1024

    def __init__(self, encoding = "utf-8", chunksize=None):
        self._encoding = encoding
        if chunksize:
            self._chunksize = chunksize
        else:
            self._chunksize = self.CHUNK_SIZE

    def download_chunks(self, url):
        filename = local_path(url)
        # NOTE the stream=True parameter below
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            for chunk in r.iter_content(chunk_size=self._chunksize):
                if chunk:
                    yield chunk

    def download_lines(self, url):
        filename = local_path(url)
        # NOTE the stream=True parameter below
        r = requests.get(url, stream=True)

        for line in r.iter_lines():
            if line:
                yield f"{line.decode(self._encoding)}\n"

    def download_url(self, url, target_filename=None):
        if target_filename is None:
            filename = local_path(url)
        else:
            filename = target_filename
        with open(filename, 'wb') as f:
            for i, chunk in enumerate(self.download_chunks(url), 1):
                f.write(chunk)
        return filename


class GDELTFilter(Enum):


    all = "all"
    gkg = "gkg"
    mentions = "mentions"
    export = "export"

    def __str__(self):
        return self.value


class GDELTChecksumError(ValueError):
    pass


class GDELTZipError(ValueError):
    pass


class GDELTFile:
    TEST_FILES = """150383 297a16b493de7cf6ca809a7cc31d0b93 http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip
318084 bb27f78ba45f69a17ea6ed7755e9f8ff http://data.gdeltproject.org/gdeltv2/20150218230000.mentions.CSV.zip
10768507 ea8dde0beb0ba98810a92db068c0ce99 http://data.gdeltproject.org/gdeltv2/20150218230000.gkg.csv.zip
"""

    def __init__(self, url:str, size:int, md5:str, gfilter: GDELTFilter = GDELTFilter.all):
        self._url = url
        self._size = size
        self._md5 = md5
        filename_with_args = url.split('/')[-1]
        self._zip_filename = filename_with_args.split('?')[0]
        self._csv_filename = os.path.splitext(self._zip_filename)[0]
        self._wd = WebDownload()
        self._filter = gfilter

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, rhs:GDELTFilter):
        self._filter = rhs

    @property
    def url(self):
        return self._url

    @property
    def size(self):
        return self._size

    @property
    def md5(self):
        return self._md5

    @property
    def zip_filename(self):
        return self._zip_filename

    @property
    def csv_filename(self):
        return self._csv_filename

    def download_file(self):
        print(f"{self.url} --> ", end="")
        self._zip_filename = self._wd.download_url(self.url)
        if not self.is_valid_checksum():
            raise GDELTChecksumError(self.url)
        print(f"{self.zip_filename}")
        return self.zip_filename

    def is_valid_checksum(self):
        computed_md5 = compute_md5(self._zip_filename)
        return computed_md5 == self.md5

    def process_zip_file(self, overwrite: bool = True):
        #
        # If overwrite download and extract
        # else
        if overwrite:
            self._zip_filename = self.download_file()
            self._csv_filename = self.extract_csv_file()
            return self.csv_filename

        elif os.path.exists(self.csv_filename):
            print(f"{self.csv_filename} exists")
        elif os.path.exists(self.zip_filename):
            print(f"{self.zip_filename} exists")
            csv_filename = self.extract_csv_file()
        else:
            self._zip_filename = self.download_file()

            self._csv_filename = self.extract_csv_file()
        return self._csv_filename

    @staticmethod
    def unzip(filename: str):
        zfilename = None
        with zipfile.ZipFile(filename) as archive:
            if len(archive.namelist()) > 1:
                raise GDELTZipError(f"More than one file in archive: {filename}")
            for zfilename in archive.namelist():
                text = archive.read(zfilename)  # .decode(encoding="utf-8")
                print(f"extracting: '{zfilename}'")
                with open(zfilename, "wb") as output_file:
                    output_file.write(text)
        return zfilename

    def extract_csv_file(self):
        self._csv_filename = GDELTFile.unzip(self.zip_filename)
        return self._csv_filename

    @classmethod
    def get_input_files(cls, f: str, last : int):
        lines = []
        with open(f, "r") as input_file:
            for input_line in input_file:
                lines.append(input_line)
            if last > 0:
                section = len(lines) - (last * 3)  # three files per set, gkg, export, mentions
                lines = lines[section:]  # slice the last days
        return lines


def download_gdelt_files(file_list: List[str], last=None, filter:GDELTFilter=GDELTFilter.all,  overwrite=False):

    if last is None or last < 0:
        last = 0

    csv_files: list[str] = []
    for f in file_list:
        lines = GDELTFile.get_input_files(f, last)
        # with open(f, "r") as input_file:
        #     for input_line in input_file:
        #         lines.append(input_line)
        #
        #     if last > 0:
        #         section = len(lines) - (last * 3)  # three files per set, gkg, exports, mentions
        #         lines = lines[section:]  # slice the last days

        for l in lines:
            try:
                size, md5, zipurl = l.split()
                gdelt_file = GDELTFile(zipurl, int(size), md5, filter)
                # print(f"{size}:{sha}:{zip}")
                if (gdelt_file.filter.value in zipurl) or (gdelt_file.filter == GDELTFilter.all):
                    f = gdelt_file.process_zip_file(overwrite)
                    csv_files.append(f)

            except zipfile.BadZipfile as e:
                print(gdelt_file.zip_filename)
                print(e)
                sys.exit(1)
            except exceptions.HTTPError as e:
                print(f"Error for {zipurl}")
                print(e)
                sys.exit(1)
            except GDELTChecksumError as e:
                print(f"'{gdelt_file.md5}' checksum for {gdelt_file.url} doesn't match\n"
                      f" checksum for {gdelt_file.zip_filename}")
                sys.exit(1)
    return csv_files

