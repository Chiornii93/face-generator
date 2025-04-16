from fastapi import FastAPI
from runpod.serverless import start
import time

app = FastAPI()

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.post("/run")
def run_job():
    time.sleep(5)  # симуляция работы
    return {"result": "Job complete."}

start(app)
