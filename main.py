from fastapi import FastAPI, UploadFile, File, HTTPException
import shutil
import os
import json
import uuid

from engines.engine_factory import get_engine
from engines.base.rubric_engine import RubricEngine

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/evaluate_excel")
async def evaluate_excel(file: UploadFile = File(...)):

    try:
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.xlsx"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Load rules
        with open("assignments/excel_101/rules.json") as f:
            rules = json.load(f)

        assignment_type = rules["assignment_type"]

        engine = get_engine(assignment_type, file_path, rules)
        rule_results = engine.evaluate()

        rubric = RubricEngine(rule_results)
        final_report = rubric.generate_report()
        print("RULE RESULTS:", rule_results)
        return {
            "status": "success",
            "data": final_report
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))