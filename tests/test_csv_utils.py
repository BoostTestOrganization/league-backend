import pytest
import re

from app.csv_utils import CSVUtil, fetch_formatted_stream_data
from functools import reduce
from itertools import chain
from operator import mul


class TestCSVUtil:

    @pytest.fixture
    def csvutil(self, csv_file):
        yield CSVUtil(csv_file)

    def test_echo(self, csvutil, csv_data_list):
        assert list(chain(csvutil.echo())) == list(chain(csv_data_list))
        for index, data in enumerate(
            fetch_formatted_stream_data(chain(csvutil.echo()))
        ):
            assert data == ",".join(csv_data_list[index]) + "\n"

    def test_inverse(self, csvutil, csv_data_list):
        inverted_list = list(chain(csvutil.invert()))
        assert list(zip(*chain(csv_data_list))) == inverted_list
        for index, data in enumerate(
            fetch_formatted_stream_data(chain(csvutil.invert()))
        ):
            assert data == ",".join(inverted_list[index]) + "\n"
    
    def test_flatten(self, csvutil, data):
        assert csvutil.flat() == ",".join(data)
    
    def test_sum(self, csvutil, data):
        assert csvutil.sum() == sum(map(int, data))
    
    def test_multiply(self, csvutil, data):
        assert csvutil.multiply() == reduce(mul, map(int, data))


class TestCSVUtilAlphanumeric:

    def test_invalid_file(self, invalid_file):
        with pytest.raises(OSError, match="Invalid extension"):
            CSVUtil(invalid_file)
    
    def test_invalid_file(self, tmp_path):
        dir = tmp_path / "dir"
        dir.mkdir()
        with pytest.raises(IsADirectoryError, match="Not a file"):
            CSVUtil(dir)
    
    def test_echo_alphanumeric_input_file(self, alphanumeric_input_file):
        assert list(chain(CSVUtil(alphanumeric_input_file).echo())) == [
            ["1", "2", "c"],
            ["01", "c84766ca4a3ce52c3602bbf02ad1f7", "Hello this is a backend coding challenge"]
        ]
    def test_inverse_alphanumeric_input_file(self, alphanumeric_input, alphanumeric_input_file):
        assert list(chain(CSVUtil(alphanumeric_input_file).invert())) == list(zip(*chain(map(str, d) for d in alphanumeric_input)))
    
    def test_flatten_alphanumeric_input_file(self, alphanumeric_input_file):
        assert CSVUtil(alphanumeric_input_file).flat() == ",".join([
            "1", "2", "c", "01", "c84766ca4a3ce52c3602bbf02ad1f7", "Hello this is a backend coding challenge"
        ])
    
    def test_sum_alphanumeric_input_file(self, alphanumeric_input_file):
        with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'c'")):
            CSVUtil(alphanumeric_input_file).sum()
    
    def test_multiply_alphanumeric_input_file(self, alphanumeric_input_file):
        with pytest.raises(ValueError, match=re.escape("invalid literal for int() with base 10: 'c'")):
            CSVUtil(alphanumeric_input_file).multiply()