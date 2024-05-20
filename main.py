import logging
import multiprocessing
from datetime import datetime
import time

from fastapi import FastAPI
from requestmodel import InputModel
from responsemodel import OutputModel

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#API to run addition in batch using multiprocess
@app.post("/", response_model=OutputModel)
async def batch_process(request: InputModel):
    logger.info(f"Received request with batch ID: {request.batchid}")
    started_at = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    try:
        with multiprocessing.Pool() as pool:
            results = pool.map(addition, request.payload)
        logger.info(f"Successfully processed batch ID: {request.batchid}")
        completed_at = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        return OutputModel(batchid=request.batchid, response=results, status="completed", started_at=started_at, completed_at=completed_at)
    except Exception as e:
        logger.error(f"An error occurred while processing the payload for batch ID {request.batchid}: {e}")
        results = []
        completed_at = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        return OutputModel(batchid=request.batchid, response=results, status="Failed", started_at=started_at, completed_at=completed_at)
    
# Addition function which retrurns addition of two numbers
def addition(numbers):
    try:
        result = numbers[0] + numbers[1]
        return result
    except Exception as e:
        logger.error(f"Error in addition function with input {numbers}: {e}")
        return f"Error: {e}"