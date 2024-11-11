#!/bin/bash
uri="${URI:=http://0.0.0.0}"

printf "Ouptut for echo:"
curl -H "Content-type: multipart/form-data" -F "upload_file=@$PWD/matrix.csv" -X POST "$uri:8000/echo"

printf "Ouptut for invert:"
curl -H "Content-type: multipart/form-data" -F "upload_file=@$PWD/matrix.csv" -X POST "$uri:8000/invert"

printf "Ouptut for flatten:"
curl -H "Content-type: multipart/form-data" -F "upload_file=@$PWD/matrix.csv" -X POST "$uri:8000/flatten"

printf "Ouptut for sum:"
curl -H "Content-type: multipart/form-data" -F "upload_file=@$PWD/matrix.csv" -X POST "$uri:8000/sum"

printf "\nOuptut for multiply:"
curl -H "Content-type: multipart/form-data" -F "upload_file=@$PWD/matrix.csv" -X POST "$uri:8000/multiply"
