import csv
import tempfile
import shutil
from functools import reduce
from itertools import chain
from operator import mul
from pathlib import Path, PosixPath

from starlette.datastructures import UploadFile


def fetch_formatted_stream_data(chain_iterables):
    """
    Parameters:
    -----------
    chain_iterables: list of iterables that will be used together to return the final output
    """
    for data in chain(chain_iterables):
        yield ",".join(map(str, data)) + "\n"


class CSVUtil:
    """
    Responsible for csv related operations
    Methods
    -------
    _validate_and_get(csvfile)
        take incoming csvfile as input file object of either type 
        PosixPath or UploadFile and returns an appropriate file object 
        that can be used to do operations on

    _check_upload_file(csvfile)
        UploadFile type Validator
    
    _check_posix_path_file(csvfile)
        PosixPath type validator
    
    _chunk_reader(csvfile, chunk_size, operation)
        Basic chunking opeation on csv reader object with a default chunk size and list operation params
    
    flatten(csvfile)
        a geenrator that returns an unwrapped flat list of values of the csv file contents
    
    echo(csvfile)
        generator that returns the contents of the csvfile
    
    invert(csvfile)
        geenrator that returns the trnaspose contents of the csvfile
    
    flat(csvfile)
        a formatted list of the flatten results that I use for testing
    
    sum(csvfile)
        sum of all the numbers in the csv file
    
    multiply(csvfile)
        product of all the numbers in the csv file
    """
    def __init__(self, csvfile):
       self.csvfile = self._validate_and_get(csvfile)

    def _validate_and_get(self, csvfile):
        if isinstance(csvfile, PosixPath):
            self._check_posix_path_file(csvfile)
            return csvfile
        elif isinstance(csvfile, UploadFile):
            self._check_upload_file(csvfile)
            # need to persist spooled temp file becasue it only exists in memory for dmall sizes
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                shutil.copyfileobj(csvfile.file, temp_file)
            return temp_file.name
        else:
            raise TypeError("Invalid file type")
    
    def _check_upload_file(self, csvfile):
        if not csvfile.filename.lower().endswith(".csv"):
            raise OSError("Invalid extension")
    
    def _check_posix_path_file(self, csvfile):
        path = Path(csvfile)
        if path.is_dir():
            raise IsADirectoryError("Not a file")
        if not path.suffix == ".csv":
            raise OSError("Invalid extension")

    def _chunk_reader(self, csv_iterable, chunk_size=1000, operation="append"):
        chunk = []
        for index, row in enumerate(csv_iterable):
            getattr(chunk, operation)(row)
            if (index + 1) % chunk_size == 0:
                yield chunk
                chunk = []
        if chunk: 
            yield chunk
    
    def flatten(self):
        with open(self.csvfile) as csvfile:
            for chunk in self._chunk_reader(csv.reader(csvfile), operation="extend"):
                yield chunk
    
    def echo(self):
         with open(self.csvfile) as csvfile:
            for chunk in self._chunk_reader(csv.reader(csvfile)):
                for row in chunk:
                    yield row
    
    def invert(self):
        with open(self.csvfile) as csvfile:
            for chunk in self._chunk_reader(zip(*csv.reader(csvfile))):
                for row in chunk:
                    yield row
    
    def flat(self):
        return ",".join(map(str, chain.from_iterable(self.flatten())))

    def sum(self):
        return sum(chain.from_iterable(map(int, s) for s in self.flatten()))
    
    def multiply(self):
        return reduce(mul, chain.from_iterable(map(int, s) for s in self.flatten()))
