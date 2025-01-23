from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    
    content = await file.read()
    buffer = io.BytesIO(content)
    
    if file_ext == "csv":
        df = pd.read_csv(buffer)
    elif file_ext == "xlsx":
        df = pd.read_excel(buffer, engine="openpyxl")
    
    return {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}
