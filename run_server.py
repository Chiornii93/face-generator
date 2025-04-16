from fastapi import FastAPI
import time

app = FastAPI()

@app.get("/")
def healthcheck():
    return {"status": "ok"}

@app.post("/run")
def run_job():
    time.sleep(5)  # симулируем работу
    return {"result": "Job complete."}
