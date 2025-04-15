from fastapi import FastAPI
from fastapi.responses import FileResponse
import subprocess
import time
import os

app = FastAPI()

COMFY_PATH = "/workspace/ComfyUI"
OUTPUT_DIR = os.path.join(COMFY_PATH, "output", "AceFaceSwap")

@app.post("/generate")
async def generate():
    # Очистка output
    if os.path.exists(OUTPUT_DIR):
        for file in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, file))
    else:
        os.makedirs(OUTPUT_DIR)

    # Запуск ComfyUI с заранее загруженным workflow
    subprocess.run(
        ["python3", "main.py", "--workflow", "face-generator-with-mask.json"],
        cwd=COMFY_PATH
    )

    # Ждём результат
    timeout = 30
    start = time.time()
    result_path = None

    while time.time() - start < timeout:
        files = os.listdir(OUTPUT_DIR)
        if files:
            result_path = os.path.join(OUTPUT_DIR, files[0])
            break
        time.sleep(1)

    if result_path:
        return FileResponse(result_path)
    else:
        return {"error": "No output generated"}
