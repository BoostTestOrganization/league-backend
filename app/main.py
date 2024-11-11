from itertools import chain
import logging
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.csv_utils import CSVUtil, fetch_formatted_stream_data

app = FastAPI()
logger = logging.getLogger("league")

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except (IsADirectoryError, OSError, ValueError) as e:
            # Log the exception for debugging
            logger.exception(e)
            return JSONResponse(status_code=400, content={"error": str(e)})
            
app.add_middleware(ExceptionHandlingMiddleware)


@app.post("/echo")
async def echo(upload_file: UploadFile):
    return StreamingResponse(
        fetch_formatted_stream_data(
            CSVUtil(upload_file).echo()
        ), 
        media_type="text/plain"
    )

@app.post("/invert")
async def invert(upload_file: UploadFile):
    return StreamingResponse(
        fetch_formatted_stream_data(
            CSVUtil(upload_file).invert()
        ), 
        media_type="text/plain"
    )


@app.post("/flatten")
async def flatten(upload_file: UploadFile):
    return StreamingResponse(
        fetch_formatted_stream_data(
            CSVUtil(upload_file).flatten()
        ), 
        media_type="text/plain"
    )


@app.post("/sum")
async def sum(upload_file: UploadFile):
    return CSVUtil(upload_file).sum()


@app.post("/multiply")
async def multiply(upload_file: UploadFile):
    return CSVUtil(upload_file).multiply()