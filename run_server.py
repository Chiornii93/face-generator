from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import uvicorn
import os
import shutil
import subprocess
import time

app = FastAPI()

@app.post("/generate")
async def generate(face: UploadFile = File(...)):
    input_dir = "ComfyUI/input"
    output_dir = "ComfyUI/output/AceFaceSwap"

    # Очистить input
    if os.path.exists(input_dir):
        shutil.rmtree(input_dir)
    os.makedirs(input_dir, exist_ok=True)

    # Очистить output
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Сохраняем файл лица
    face_path = os.path.join(input_dir, face.filename)
    with open(face_path, "wb") as f:
        f.write(await face.read())

    # Запускаем ComfyUI через команду
    subprocess.run(["python3", "main.py", "--workflow", "face-generator-with-mask.json"], cwd="ComfyUI")

    # Ждём появления выходного файла
    timeout = 30
    start = time.time()
    result_path = None

    while time.time() - start < timeout:
        files = os.listdir(output_dir)
        if files:
            result_path = os.path.join(output_dir, files[0])
            break
        time.sleep(1)

    if result_path:
        return FileResponse(result_path)
    else:
        return {"error": "No output generated."}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
