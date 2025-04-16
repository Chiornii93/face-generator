from runpod.serverless import start, handler
import subprocess
import os
import time

COMFY_PATH = "/workspace/ComfyUI"
WORKFLOW_NAME = "face-generator-with-mask.json"
OUTPUT_DIR = os.path.join(COMFY_PATH, "output", "AceFaceSwap")

def run_comfyui(job):
    # Очистка output
    if os.path.exists(OUTPUT_DIR):
        for item in os.listdir(OUTPUT_DIR):
            os.remove(os.path.join(OUTPUT_DIR, item))
    else:
        os.makedirs(OUTPUT_DIR)

    # Запуск workflow
    subprocess.run([
        "python3", "main.py", "--workflow", WORKFLOW_NAME
    ], cwd=COMFY_PATH)

    # Ожидание результата
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = os.listdir(OUTPUT_DIR)
        if files:
            return {"result": files[0]}  # Просто возвращаем имя файла
        time.sleep(1)

    return {"error": "No output generated."}

handler.register(run_comfyui)
start()
