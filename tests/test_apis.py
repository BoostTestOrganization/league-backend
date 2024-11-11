
class TestAPI:
    def test_echo(self, client, api_csv_file):
        response = client.post("/echo",files={
            "upload_file": (api_csv_file.as_posix(), api_csv_file.open("rb"), "text/csv")
        })
        assert response.status_code == 200
        assert response.text == "1,2,3\n4,5,6\n7,8,9\n"

    def test_invert(self, client, api_csv_file):
        response = client.post("/invert",files={
            "upload_file": (api_csv_file.as_posix(), api_csv_file.open("rb"), "text/csv")
        })
        assert response.status_code == 200
        assert response.text == "1,4,7\n2,5,8\n3,6,9\n"

    def test_flatten(self, client, api_csv_file):
        response = client.post("/flatten",files={
            "upload_file": (api_csv_file.as_posix(), api_csv_file.open("rb"), "text/csv")
        })
        assert response.status_code == 200
        assert response.text == "1,2,3,4,5,6,7,8,9\n"

    def test_sum(self, client, api_csv_file):
        response = client.post("/sum",files={
            "upload_file": (api_csv_file.as_posix(), api_csv_file.open("rb"), "text/csv")
        })
        assert response.status_code == 200
        assert response.text == "45"
    
    def test_multiply(self, client, api_csv_file):
        response = client.post("/multiply",files={
            "upload_file": (api_csv_file.as_posix(), api_csv_file.open("rb"), "text/csv")
        })
        assert response.status_code == 200
        assert response.text == "362880"
    
    def test_multiply_invalid_input(self, client, alphanumeric_input_file):
        response = client.post("/multiply",files={
            "upload_file": (alphanumeric_input_file.as_posix(), alphanumeric_input_file.open("rb"), "text/csv")
        })
        assert response.status_code == 400
        assert response.json() == {"error": "invalid literal for int() with base 10: 'c'"}
    
    def test_invalid_file_upload(self, client, invalid_file):
        response = client.post("/multiply",files={
            "upload_file": (invalid_file.as_posix(), invalid_file.open("rb"), "text/csv")
        })
        assert response.status_code == 400
        assert response.json() == {"error": "Invalid extension"}
