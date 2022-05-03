import unittest
import os
from gdelttools.web import WebDownload, local_path


class TestDownload(unittest.TestCase):

    photo_name = "london.jpg"
    photo_url= "https://jdrumgoole.files.wordpress.com/2018/10/20180927_173519.jpg"
    text_filename = "testmasterfilelist.txt"
    text_url = "http://joedrumgoole.com/testmasterfilelist.txt"

    def setUp(self):
        self._wd = WebDownload()

    def test_local_path(self):
        p = local_path(self.photo_url)
        self.assertEqual(p, "20180927_173519.jpg")

    def test_download_chunks(self):
        if os.path.exists(self.photo_name):
            os.unlink(self.photo_name)
        self._wd.download_url(self.photo_url, self.photo_name)
        self.assertTrue(os.path.exists(self.photo_name))
        os.unlink(self.photo_name)

    def test_download_lines(self):
        if os.path.exists(self.text_filename):
            os.unlink(self.text_filename)
        with open(self.text_filename, "w") as output_file:
            for i,line in enumerate(self._wd.download_lines(self.text_url), 1):
                output_file.write(f"{line}")
            self.assertEqual(i, 2000)
        self.assertEqual(os.path.getsize(self.text_filename), 213940)
        os.unlink(self.text_filename)

    def test_download_url(self):
        self._wd.download_url(self.text_url, self.text_filename+"1")
        url_size = os.path.getsize(self.text_filename+"1")
        self.test_download_lines()
        line_size = os.path.getsize(self.text_filename+"1")
        self.assertEqual(url_size, line_size)
        os.unlink(self.text_filename+"1")

if __name__ == '__main__':
    unittest.main()
