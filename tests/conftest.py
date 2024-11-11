import csv
import pytest

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def data():
    # data from 0 to 100
    yield [str(index) for index in range(100)]


@pytest.fixture
def csv_data_list(data):
    rows = 10
    # matrix data will contain list of lists
    matrix_data = []
    sub_matrix_data = []
    # each row will have 10 values
    for index, value in enumerate(data):
        if index % rows == 0 and index > 0:
            matrix_data.append(sub_matrix_data)
            sub_matrix_data = []
        sub_matrix_data.append(value)
    if sub_matrix_data:
        matrix_data.append(sub_matrix_data)
    yield matrix_data


@pytest.fixture
def csv_file(csv_data_list, tmp_path):
    csvfile = tmp_path / "test_matrix.csv"
    csvfile.touch()
    with open(csvfile, "w") as f:
        csv.writer(f).writerows(csv_data_list)
    yield csvfile


@pytest.fixture
def invalid_file(tmp_path):
    p = tmp_path / "hello.txt"
    p.write_text("hello", encoding="utf-8")
    yield p


@pytest.fixture
def alphanumeric_input():
    yield [
        [1, "2", "c"],
        ["01", "c84766ca4a3ce52c3602bbf02ad1f7", "Hello this is a backend coding challenge"]
    ]


@pytest.fixture
def alphanumeric_input_file(alphanumeric_input, tmp_path):
    csvfile = tmp_path / "matrix.csv"
    csvfile.touch()
    with open(csvfile, "w") as f:
        csv.writer(f).writerows(alphanumeric_input)
    yield csvfile


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def api_csv_file(csv_data_list, tmp_path):
    csvfile = tmp_path / "test_api_matrix.csv"
    csvfile.touch()
    rows = [
        [1,2,3],
        [4,5,6],
        [7,8,9]
    ]
    with open(csvfile, "w") as f:
        csv.writer(f).writerows(rows)
    yield csvfile
