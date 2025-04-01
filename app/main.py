from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict
import shutil
import os
from app.spark_queries import filter_zipcodes

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="PySpark CSV Query API")

@app.post("/upload/")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV.")
    
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_location}

@app.get("/zipcodes/{filename}/{zipcode}", response_model=List[Dict])
def query_zipcodes(filename: str, zipcode: int):
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="CSV file not found.")

    try:
        results = filter_zipcodes(file_path, zipcode)
        if not results:
            return JSONResponse(content={"detail": "No matching zipcodes found."}, status_code=404)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
