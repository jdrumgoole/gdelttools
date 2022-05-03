import unittest

from gdelttools.mongoimport import MongoImport, BinaryNotFoundError


class TestMongoImport(unittest.TestCase):
    def test_mongoimport(self):

        with self.assertRaises(BinaryNotFoundError):
            x = MongoImport(prog="notmongoimport")  # add assertion here


if __name__ == '__main__':
    unittest.main()
