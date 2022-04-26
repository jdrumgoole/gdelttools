
import urllib
from io import BytesIO
import os

import zipfile
import requests


def download_and_unzip(u: str):
    url_file = urllib.request.urlopen(u)

    with zipfile.ZipFile(BytesIO(url_file.read())) as my_zip_file:
        my_zip_file.extractall()


def skip_this_file(zip_filename: str, overwrite: bool = None):
    name, ext = os.path.splitext(zip_filename)
    csv_filename = f"{name}.CSV"
    if overwrite:
        return overwrite
    else:
        name, ext = os.path.splitext(zip_filename)
        csv_filename = f"{name}.CSV"
        return os.path.exists(zip_filename) or os.path.exists(csv_filename)


def local_path(url):
    filename_with_args = url.split('/')[-1]
    filename = filename_with_args.split('?')[0]
    return filename


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




