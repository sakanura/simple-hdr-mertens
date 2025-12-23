from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import cv2
import numpy as np
from hdr_utils import process_hdr

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Serve output files as static
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")


@app.post("/api/hdr")
async def create_hdr(files: list[UploadFile] = File(...)):
    if len(files) < 3:
        return JSONResponse({"error": "Need at least 3 images."}, status_code=400)

    images = []
    for f in files:
        content = await f.read()
        np_img = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
        images.append(img)

    hdr_path, hist_path, compare_path = process_hdr(images)

    return {
        "hdr_result": hdr_path,
        "histogram": hist_path,
        "compare": compare_path
    }


@app.get("/api/download/{filename}")
def download_file(filename: str):
    return FileResponse(f"./outputs/{filename}", filename=filename)
