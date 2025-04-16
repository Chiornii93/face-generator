from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Hello from RunPod!"}

@app.post("/run")
def run_workflow():
    return {"status": "ready", "message": "This is where ComfyUI will run."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
