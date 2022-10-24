"""A main script to run api.

"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from src.utility.loggers import logger
from src.inference.core import generate_output


class InputData(BaseModel):
    """A class to define data and it's type for input data.

    Args:
        BaseModel :  A base datatype class
    """

    data: str


app = FastAPI()


@app.get("/")
async def read_root():
    """basic server health check url

    Returns:
        dict : A message that server is running
    """

    logger.info("API server is running.")
    return {"msg": "API server is running"}


@app.post("/model_inference/")
async def get_model_output(input_data: InputData):
    """A method to return model response on API request

    Args:
        input_data (str): Input data required for model
    Returns:
        dict : model output

    """

    try:
        output = generate_output(input_data.data)
        return {"model_output": output}
    except Exception as error:
        message = "Error while creating output"
        logger.error(message, str(error))


# This is used only for unit testing the application/
# or for running this app as standalone instead of via docker
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
