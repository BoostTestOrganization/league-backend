# League Backend Challenge

In main.go you will find a basic web server written in GoLang. It accepts a single request _/echo_. Extend the webservice with the ability to perform the following operations

Given an uploaded csv file
```
1,2,3
4,5,6
7,8,9
```

1. Echo (given)
    - Return the matrix as a string in matrix format.
    
    ```
    // Expected output
    1,2,3
    4,5,6
    7,8,9
    ``` 
2. Invert
    - Return the matrix as a string in matrix format where the columns and rows are inverted
    ```
    // Expected output
    1,4,7
    2,5,8
    3,6,9
    ``` 
3. Flatten
    - Return the matrix as a 1 line string, with values separated by commas.
    ```
    // Expected output
    1,2,3,4,5,6,7,8,9
    ``` 
4. Sum
    - Return the sum of the integers in the matrix
    ```
    // Expected output
    45
    ``` 
5. Multiply
    - Return the product of the integers in the matrix
    ```
    // Expected output
    362880
    ``` 

The input file to these functions is a matrix, of any dimension where the number of rows are equal to the number of columns (square). Each value is an integer, and there is no header row. matrix.csv is example valid input.  

Run web server
```
go run .
```

Send request
```
curl -F 'file=@/path/matrix.csv' "localhost:8080/echo"
```

## What we're looking for

- The solution runs
- The solution performs all cases correctly
- The code is easy to read
- The code is reasonably documented
- The code is tested
- The code is robust and handles invalid input and provides helpful error messages


## Code built using:
- python 3.13
- docker

## Pre requisites to run the code:
- docker
- for local development in your machine without containerization you need
  - pyenv
  - pip-tools
  - Create a virtualenv using pyenv: `pyenv virtualenv 3.13.0 league-backend`
  - Activate using `pyenv activate league-backend`
  - run tests: `pyest -svv .`
  - run local script to see output of all endpoints:
    - `cd scripts`
    - `./curl_script.sh`
- using docker all you need to do to run:
  - To see test results: `docker compose run test`
  - To see curl outputs: `docker compose run curlrunner`
- You can find the url to the web app at: `http://0.0.0.0:8000`
  - you can find the docs at: `http://0.0.0.0:8000/docs`
  
## Considerations:
- I left the api responses as text since I saw no context about the kind of return type expected
- I'm returning the error as json responses
- I'm chuking csv because there's no mention of how big the files can be.
- I'm returning streaing responses for endpoints that I believe might end up having large batches of data at scale
- I have a few methods that I'm using purely for easier testing
- I have testing for the `csv_utils.py` and the `main.py` which covers the csv utility requirements asked by the challenege and the api calls respectively.
- I would have lived to add linting and strict type checking but I am travelling currently and I can only think to spend so much time on a take home project.
- I left the go file as is in the project since the script came with the email. Would have loved to explore the possibilites with go in this project but I am pressed for time
