from datetime import datetime
from gdelttools.web import WebDownload
import requests


class GDELTWebData:

    gdelt_md5_list = "http://data.gdeltproject.org/events/md5sums"
    gdelt_file_sizes = "http://data.gdeltproject.org/events/filesizes"
    checksum_filename = "gdelt_md5sums"
    size_filename = "gdelt_filesizes"

    master_url = "http://data.gdeltproject.org/gdeltv2/masterfilelist.txt"
    update_url = "http://data.gdeltproject.org/gdeltv2/lastupdate.txt"

    downloader = WebDownload()

    @classmethod
    def get_metadata(cls):
        # size and MD5 checksums to validate downloads
        r = requests.get(cls.gdelt_md5_list, allow_redirects=True)
        with open(cls.checksum_filename, "w") as output_file:
            output_file.write(r.content.decode("utf-8"))
        r = requests.get(cls.gdelt_file_sizes, allow_redirects=True)
        with open(cls.size_filename, "w") as output_file:
            output_file.write(r.content.decode("utf-8"))
        return [cls.checksum_filename, cls.size_filename]

    @classmethod
    def get_update_list(cls, overwrite=False):
        return cls.downloader.download_url(cls.update_url)

    @classmethod
    def get_master_list(cls, overwrite=False):
        return cls.downloader.download_url(cls.master_url)

