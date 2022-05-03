import os
from enum import Enum
import shutil
import glob

class BinaryNotFoundError(OSError):
    pass

class FileType(Enum):
    tsv = "tsv"
    csv = "csv"

    def __str__(self):
        return self.value


class InsertMode(Enum):
    upsert = "upsert"

    def __str__(self):
        return self.value




class MongoImport:
    '''
    Implement this script for mongoimport. We expect mongoimport to be installed
    and be available on the path.

    mongoimport --db=GDELT2 --collection=eventscsv  --type=tsv --fieldFile=gdelt_field_file.ff --mode=upsert --writeConcern "{w:1}" --columnsHaveTypes --file=$i $*
    '''

    def __init__(self,
                 prog: str = "mongoimport",
                 uri: str = "mongodb://localhost:27017",
                 database_name: str="GDELT2",
                 collection_name: str="eventscsv",
                 file_type : FileType = FileType.tsv,
                 field_file: str = "gdelt_field_file.ff",
                 insert_mode : InsertMode = InsertMode.upsert,
                 write_concern : str = "{w:1}"):
        """
        Define init parameters for mongoimport command
        :param database: The mongodb database name we will be importing to
        :param collection: The collection name we will be importing to
        """

        self._prog = prog
        self._uri = uri
        self._database_name = database_name
        self._collection_name = collection_name
        self._file_type = file_type
        self._field_file = field_file
        self._insert_mode = insert_mode
        self._write_concern = write_concern

        if shutil.which(self._prog) is None:
            raise BinaryNotFoundError(f"{self._prog}: Cannot be found on the current PATH")

    def command(self, input_file:str):

        return f"mongoimport --uri {self._uri} --db {self._database_name} --collection {self._collection_name} " +\
               f"--type {self._file_type.value} --fieldFile {self._field_file} " +\
               f"--mode {self._insert_mode.value} --writeConcern '{self._write_concern}' --columnsHaveTypes " +\
               f"--file {input_file}"

    def import_data(self, arg:str):
        args = glob.glob(arg)
        for i in args:
            print(f"Running in: {os.getcwd()}")
            print(self.command(i))
            os.system(f"{self.command(i)}")


if __name__ == "__main__":
    m = MongoImport()
    m.import_data("*.export.CSV")

