from fastapi import FastAPI
from Model import download_and_calc

app = FastAPI()


@app.post("/calculate/")
async def calculate(input_string: str):
    result = download_and_calc(input_string)
    return result
