import tempfile
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import traceback

from fastapi.middleware.cors import CORSMiddleware
import io
from fastapi.responses import JSONResponse

import pyreadstat
import xport
import xport.v56

import numpy as np

app = FastAPI()

def sanitize_dataframe(df):
    df = df.replace([np.inf, -np.inf, np.nan], None)
    df = df.applymap(lambda x: None if isinstance(x, float) and (np.isnan(x) or np.isinf(x)) else x)  # додаємо перевірку на NaN та Inf
    return df

def sanitize_for_json(data):
    def safe_value(val):
        if isinstance(val, float) and (np.isnan(val) or np.isinf(val)):
            return None
        return val

    return {key: [safe_value(item) for item in value] for key, value in data.items()}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_ext = file.filename.split(".")[-1]
    
    content = await file.read()
    buffer = io.BytesIO(content)
    
    try:        
        if file_ext == "csv":
            df = pd.read_csv(buffer)
        elif file_ext == "xlsx":
            df = pd.read_excel(buffer, engine="openpyxl")
        elif file_ext == "sas7bdat":
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(content)
                temp_file.close() 
                df, _ = pyreadstat.read_sas7bdat(temp_file.name)
        elif file_ext == "xpt":
            print(f"Attempting to process XPT file: {file.filename}")
            reader = xport.Reader(buffer)
            records = list(reader)
            df = pd.DataFrame.from_records(records)
        else:
            return JSONResponse(status_code=400, content={"error": "Непідтримуваний формат файлу"})
    except Exception as e:
        error_message = traceback.format_exc()
        return JSONResponse(status_code=500, content={"error": f"Помилка обробки файлу: {str(e)}"})

    df = sanitize_dataframe(df)
    
    result = {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}
    result = sanitize_for_json(result)  
    
    try:
        return JSONResponse(content=result)
    except ValueError as ve:
        return JSONResponse(status_code=500, content={"error": "Помилка при серіалізації даних до JSON."})

    # return {"columns": df.columns.tolist(), "data": df.to_dict(orient="records")}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)
