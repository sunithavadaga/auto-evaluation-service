from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import shutil
import os
import json
import uuid

from services.database import get_db
from services.models import Submission
from engines.engine_factory import get_engine
from engines.base.rubric_engine import RubricEngine

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/run_evaluation_batch")
def run_batch(db: Session = Depends(get_db)):
    from services.evaluation_worker import process_pending_submissions
    process_pending_submissions(db)
    return {"message": "Batch evaluation completed"}




@app.post("/submit_excel")
async def submit_excel(
    student_id: int,
    assignment_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:
        # 1️⃣ Save file
        unique_filename = f"{uuid.uuid4()}.xlsx"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 2️⃣ Create submission record
        submission = Submission(
            student_id=student_id,
            assignment_id=assignment_id,
            submission_link=file_path,
            status="submitted"
        )

        db.add(submission)
        db.commit()
        db.refresh(submission)

        # 3️⃣ Load rules dynamically (can later use assignment_id based path)
        with open("assignments/excel_101/rules.json") as f:
            rules = json.load(f)

        # 4️⃣ Run evaluation
        engine = get_engine(rules["assignment_type"], file_path, rules)
        rule_results = engine.evaluate()

        rubric = RubricEngine(rule_results)
        final_report = rubric.generate_report()

        # 5️⃣ Update submission with evaluation results
        submission.score = final_report["total_score"]
        submission.max_score = final_report["max_score"]
        submission.percentage = final_report["percentage"]
        submission.feedback = "\n".join(final_report.get("feedback", []))
        submission.evaluation_details = final_report["detailed_results"]
        submission.status = "evaluated"

        db.commit()
        db.refresh(submission)

        # 6️⃣ Return result immediately
        return {
            "submission_id": submission.id,
            "score": submission.score,
            "max_score": submission.max_score,
            "percentage": submission.percentage,
            "feedback": submission.feedback,
            "status": submission.status
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))