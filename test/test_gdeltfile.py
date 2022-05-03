import unittest
import os
import zipfile

from gdelttools.gdeltfile import GDELTFile, GDELTFilter, download_gdelt_files


class TestGDeltFile(unittest.TestCase):
    size = 150383
    md5 = "297a16b493de7cf6ca809a7cc31d0b93"
    url = "http://data.gdeltproject.org/gdeltv2/20150218230000.export.CSV.zip"

    def test_gdelt_file(self):
        f = GDELTFile(self.url, self.size, self.md5, GDELTFilter.all)
        self.assertEqual(self.url, f.url)
        self.assertEqual(self.size, f.size)
        self.assertEqual(self.md5, f.md5)
        self.assertEqual(GDELTFilter.all, f.filter)
        f = GDELTFile(self.url, self.size, self.md5, GDELTFilter.gkg)
        self.assertEqual(GDELTFilter.gkg, f.filter)
        self.assertEqual(GDELTFilter.gkg.value, "gkg")
        self.assertTrue(GDELTFilter.export.value in self.url)

    def test_download(self):
        f = GDELTFile(self.url, self.size, self.md5, GDELTFilter.all)
        f.download_file()
        self.assertTrue(os.path.isfile(f.zip_filename))
        os.unlink(f.zip_filename)

    def test_extract(self):
        f = GDELTFile(self.url, self.size, self.md5, GDELTFilter.all)
        f.download_file()
        self.assertTrue(os.path.isfile(f.zip_filename))
        f.extract_csv_file()
        self.assertTrue(os.path.isfile(f.csv_filename))
        os.unlink(f.zip_filename)
        os.unlink(f.csv_filename)

    def test_download_gdelt_files(self):

        with open("threefiles.txt", "w") as tfile:
            tfile.write(GDELTFile.TEST_FILES)

        download_gdelt_files(["threefiles.txt"], overwrite=True)
        self.assertTrue(os.path.exists("20150218230000.export.CSV.zip"))
        self.assertTrue(os.path.exists("20150218230000.mentions.CSV.zip"))
        self.assertTrue(os.path.exists("20150218230000.gkg.csv.zip"))
        os.unlink("20150218230000.export.CSV.zip")
        os.unlink("20150218230000.mentions.CSV.zip")
        os.unlink("20150218230000.gkg.csv.zip")
        os.unlink("20150218230000.export.CSV")
        os.unlink("20150218230000.mentions.CSV")
        os.unlink("20150218230000.gkg.csv")

        download_gdelt_files(["threefiles.txt"])
        self.assertTrue(os.path.exists("20150218230000.export.CSV.zip"))
        self.assertTrue(os.path.exists("20150218230000.mentions.CSV.zip"))
        self.assertTrue(os.path.exists("20150218230000.gkg.CSV.zip"))
        os.unlink("20150218230000.export.CSV.zip")
        os.unlink("20150218230000.mentions.CSV.zip")
        os.unlink("20150218230000.gkg.csv.zip")
        os.unlink("20150218230000.export.CSV")
        os.unlink("20150218230000.mentions.CSV")
        os.unlink("20150218230000.gkg.csv")

        download_gdelt_files(["threefiles.txt"], last=0, overwrite=True, filter=GDELTFilter.gkg)
        self.assertTrue(os.path.exists("20150218230000.gkg.csv.zip"))
        self.assertFalse(os.path.exists("20150218230000.export.CSV.zip"))
        self.assertFalse(os.path.exists("20150218230000.mentions.CSV.zip"))
        os.unlink("20150218230000.gkg.csv.zip")
        os.unlink("20150218230000.gkg.csv")

        download_gdelt_files(["threefiles.txt"], last=0, filter=GDELTFilter.mentions)
        self.assertFalse(os.path.exists("20150218230000.gkg.csv.zip"))
        self.assertFalse(os.path.exists("20150218230000.export.CSV.zip"))
        self.assertTrue(os.path.exists("20150218230000.mentions.CSV.zip"))
        os.unlink("20150218230000.mentions.CSV.zip")
        os.unlink("20150218230000.mentions.CSV")

        with open("threefiles.zip", "w") as tfile:
            tfile.write(GDELTFile.TEST_FILES)

        self.assertRaises(zipfile.BadZipfile, GDELTFile.unzip, "threefiles.zip")
        os.unlink("threefiles.zip")
        os.unlink("threefiles.txt")


if __name__ == '__main__':
    unittest.main()
